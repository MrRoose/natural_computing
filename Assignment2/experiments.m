%% iris
load fisheriris.mat

data = meas;
[N, D] = size(meas);

Q = 40;

quantization_errors = zeros(Q, 2);
correct = zeros(Q,2);

for q = 1:Q

    [centroids_pso] = gbest(meas, 10, 3, 1000);
    [centroids_kmeans] = kmeans(meas, 3);

    distances = zeros(N, 2);
    assignments = zeros(N, 2);

    for n  = 1:N
        data_point = data(n, :);
        cluster_dists_pso = sqrt(sum((data_point - centroids_pso).^2, 2));
        [best_dist, best_idx] = min(cluster_dists_pso);
        distances(n, 1) = best_dist;
        assignments(n, 1) = best_idx;

        cluster_dists_kmeans = sqrt(sum((data_point - centroids_kmeans).^2, 2));
        [best_dist, best_idx] = min(cluster_dists_kmeans);
        distances(n, 2) = best_dist;
        assignments(n, 2) = best_idx;
    end

    % Measure correctness of assignments

    per = perms([1 2 3]);
    best_pso = 0;
    best_kmeans = 0;
    for i = 1:size(per, 1)
        cur_perm = per(i, :);
        true_vals = zeros(N, 1);
        true_vals = true_vals + cur_perm(1) * strcmp(species, 'setosa');
        true_vals = true_vals + cur_perm(2) * strcmp(species, 'versicolor');
        true_vals = true_vals + cur_perm(3) * strcmp(species, 'virginica');
        best_pso = max(best_pso, sum(true_vals == assignments(:,1)));
        best_kmeans = max(best_kmeans, sum(true_vals == assignments(:,2)));
    end

    correct(q, 1) = best_pso;
    correct(q, 2) = best_kmeans;
    
    quantization_errors(q, 1) = quantization_error(3, distances(:,1), assignments(:,1));
    quantization_errors(q, 2) = quantization_error(3, distances(:,2), assignments(:,2));
end

mean(correct)
mean(quantization_errors)
std(quantization_errors, 0, 1)

%% Artificial problem 1
Q = 40;
N = 400;
data = -1 + 2 * rand(400, 2);
class = (data(:,1) >= 0.7 | data(:, 1) <= 0.3) & (data(:, 2) >= -0.2 - data(:,1));

quantization_errors = zeros(Q, 2);
correct = zeros(Q,2);

for q = 1:Q

    [centroids_pso] = gbest(data, 10, 2, 1000);
    [centroids_kmeans] = kmeans(data, 2);

    distances = zeros(N, 2);
    assignments = zeros(N, 2);

    for n  = 1:N
        data_point = data(n, :);
        cluster_dists_pso = sqrt(sum((data_point - centroids_pso).^2, 2));
        [best_dist, best_idx] = min(cluster_dists_pso);
        distances(n, 1) = best_dist;
        assignments(n, 1) = best_idx;

        cluster_dists_kmeans = sqrt(sum((data_point - centroids_kmeans).^2, 2));
        [best_dist, best_idx] = min(cluster_dists_kmeans);
        distances(n, 2) = best_dist;
        assignments(n, 2) = best_idx;
    end
    
    quantization_errors(q, 1) = quantization_error(2, distances(:,1), assignments(:,1));
    quantization_errors(q, 2) = quantization_error(2, distances(:,2), assignments(:,2));
    
end

mean(quantization_errors)
std(quantization_errors, 0, 1)


%% Functions

function error = quantization_error(n_clusters, distances, assignments)
    error = 0;
    for c = 1:n_clusters
            ass_to_c = find(assignments == c);
            error = error + sum(distances(ass_to_c))/sum(ass_to_c);
    end
    error = error / n_clusters;
end