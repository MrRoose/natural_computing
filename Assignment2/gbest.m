function [centroids] = gbest(data, n_particles, n_clusters, n_iters)
%GBEST Summary of this function goes here
%   data : each row is a data point

    [N, D] = size(data);

    % Values from paper
    w  = 0.72; 
    c1 = 1.49; 
    c2 = 1.49; 

    positions = zeros(n_clusters, D, n_particles);
    velocities = rand(n_clusters, D, n_particles) * 0.1;
    personal_bests = zeros(n_clusters, D, n_particles); 
    personal_best_fitness = zeros(n_particles, 1);
    global_best = zeros(n_clusters, D);
    global_best_fitness = 0;


    % We initialize using data points
    for i = 1:n_particles
        particle_starting_idxs = randsample(N, n_clusters); 
        positions(:, :, i) = data(particle_starting_idxs, :);
    end

    % calculate fitness of initializations
    distances = zeros(N, n_particles);
    assignments = zeros(N, n_particles);

    for i = 1:n_particles
            for n  = 1:N
                data_point = data(n, :);
                cluster_dists = sqrt(sum((data_point - positions(:, :, i)).^2, 2));
                [best_dist, best_idx] = min(cluster_dists);
                distances(n, i) = best_dist;
                assignments(n, i) = best_idx;
            end
    end

    personal_best_fitness = fitness(n_particles, n_clusters, distances, assignments);
    personal_bests = positions;

    for i = 1:n_iters
        for j = 1:n_particles
            for n  = 1:N
                data_point = data(n, :);
                cluster_dists = sqrt(sum((data_point - positions(:, :, j)).^2, 2));
                [best_dist, best_idx] = min(cluster_dists);
                distances(n, j) = best_dist;
                assignments(n, j) = best_idx;
            end
        end
        local_fitness = fitness(n_particles, n_clusters, distances, assignments);

        % update local global best
        for j = 1:n_particles
            if local_fitness(j) < personal_best_fitness(j)
                personal_best_fitness(j) = local_fitness(j);
                personal_bests(:, :, j) = positions(:, :, j);
            end
        end    

        [global_best_fitness, best_particle_idx] = min(personal_best_fitness);
        global_best = personal_bests(:,:, best_particle_idx);

        r1 = rand();
        r2 = rand();

        for j=1:n_particles        
            vel_part = w * velocities(:,:,j);
            cognitive_part = c1 * r1 * (personal_bests(:,:,j) - positions(:,:,j));
            social_part = c2 * r2 * (global_best - positions(:,:,j));
            velocity = vel_part + cognitive_part + social_part;

            positions(:,:,j) = positions(:,:,j) + velocity;
            velocities(:,:,j) = velocity;
        end


    end
    centroids = global_best; % we should actually do one more fitness calculation...
end

function fitness = fitness(n_particles, n_clusters, distances, assignments)
    fitness = zeros(n_particles, 1);
    for i = 1:n_particles
        for c = 1:n_clusters
            ass_to_c = find(assignments(:,i) == c);
            fitness(i) = fitness(i) + sum(distances(ass_to_c, i))/sum(ass_to_c);
        end
    end
    fitness = fitness / n_clusters;
end