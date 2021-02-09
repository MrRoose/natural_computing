clear all;
rng(3);

%File-tsp

population_size = 60;
p_elitism = 0.05; % percentage of population that will surely make it to the next population
p_c = 0.6; % probability of crossover
p_m = 0.1; % probability of mutation


cities = load('file-tsp.txt');

Q = 20; % number of experiments

% First we compare based on iterations
n_iters_ga = 1000; 
n_iters_mem = 100; % memetic algorithm is much slower
q_best_fitness_ga = zeros(Q, n_iters_ga);
q_best_fitness_mem = zeros(Q, n_iters_mem);
q_best_fitness_ga_local_search = zeros(Q, 1);
for q = 1:Q
    [final_population_ga, fitness_hist, ~] = ga(cities, n_iters_ga, 0, p_elitism, p_c, p_m, population_size); % standard
    q_best_fitness_ga(q, :) = fitness_hist;
    
    % Perform local search on the final population to see if we can find
    % some improvement there
    best_fitness_after_search = 1000;
    for i = 1:population_size
        improved_route = local_search(final_population_ga(i, :), cities);
        best_fitness_after_search = min(best_fitness_after_search, calc_dist(improved_route, cities));
    end
    q_best_fitness_ga_local_search(q) = best_fitness_after_search;
    
    [~, fitness_hist, ~] = ga(cities, n_iters_mem, 1, p_elitism, p_c, p_m, population_size); % memetic
    q_best_fitness_mem(q, :) = fitness_hist;
end

mean_fitness_ga = mean(q_best_fitness_ga, 1);
mean_fitness_mem = mean(q_best_fitness_mem, 1);
figure()
plot(1:n_iters_ga, mean_fitness_ga);
hold on
plot(1:n_iters_mem, mean_fitness_mem);
legend('GA', 'Memetic');
title('file-tsp.txt');
xlabel('Iteration');
ylabel('Best route length of generation');
hold off

avg_final_ga = mean_fitness_ga(end)
avg_final_mem = mean_fitness_mem(end)
avg_final_ga_after_search = mean(q_best_fitness_ga_local_search)


% Now we want to take into account computing time
% We have found that 1000 iterations of the standard GA takes about 1.5-2s
% Which is equal to about 60-80 iterations of the memetic algorithm
n_iters_ga = 1000;
n_iters_memetic = 80;

t_vals = 0:0.1:1.4;
t_best_fitness = zeros(length(t_vals), 2);
for q = 1:Q
    [~, fitness_hist_ga, times_ga] = ga(cities, n_iters_ga, 0, p_elitism, p_c, p_m, population_size); % standard
    [~, fitness_hist_mem, times_mem] = ga(cities, n_iters_memetic, 1, p_elitism, p_c, p_m, population_size); % memetic
    
    t_idx = 1;
    for t_val = t_vals
        first_idx = find(times_ga >= t_val, 1);
        t_best_fitness(t_idx, 1) = t_best_fitness(t_idx, 1) + fitness_hist_ga(first_idx);
        first_idx = find(times_mem >= t_val, 1);
        t_best_fitness(t_idx, 2) = t_best_fitness(t_idx, 1) + fitness_hist_mem(first_idx);
        t_idx = t_idx + 1;
    end
end
t_best_fitness = t_best_fitness / Q; % Take mean over experiments
figure()
plot(t_vals, t_best_fitness(:,1));
hold on
plot(t_vals, t_best_fitness(:,2));
legend('GA', 'memetic')
title('Computing time vs. performance')
xlabel('Computing time (s)')
ylabel('Best route length of generation')

att48 

cities = load('att48.tsp');
cities = cities(:, 2:3);

% First we compare based on iterations
n_iters_ga = 1000; 
n_iters_mem = 100; % memetic algorithm is much slower
q_best_fitness_ga = zeros(Q, n_iters_ga);
q_best_fitness_mem = zeros(Q, n_iters_mem);
for q = 1:Q
    [~, fitness_hist, ~] = ga(cities, n_iters_ga, 0, p_elitism, p_c, p_m, population_size); % standard
    q_best_fitness_ga(q, :) = fitness_hist;
    
    [~, fitness_hist, ~] = ga(cities, n_iters_mem, 1, p_elitism, p_c, p_m, population_size); % memetic
    q_best_fitness_mem(q, :) = fitness_hist;
end

mean_fitness_ga = mean(q_best_fitness_ga, 1);
mean_fitness_mem = mean(q_best_fitness_mem, 1);
figure()
plot(1:n_iters_ga, mean_fitness_ga);
hold on
plot(1:n_iters_mem, mean_fitness_mem);
legend('GA', 'Memetic');
xlabel('Iteration');
ylabel('Best route length of generation');
title('att48.tsp');
hold off

avg_final_ga = mean_fitness_ga(end)
avg_final_mem = mean_fitness_mem(end)

%% Functions
function dist = calc_dist(route, cities)
    dist = 0;
    for i = 1:length(route)-1
        city_1 = route(i);
        city_2 = route(i+1);
        dist = dist + sqrt(sum((cities(city_1,:) - cities(city_2,:)).^2));
    end
end

function new_route = local_search(route, cities)
    outer_break = 0;
    inner_break = 0;
    while ~outer_break
        best_distance = calc_dist(route, cities);
        for i = 1:length(route)
            for k = i+1:length(route)
                new_route = two_opt_swap(route, i, k);
                new_distance = calc_dist(new_route, cities);
                if new_distance < best_distance
                    route = new_route;
                    best_distance = new_distance;
                    inner_break = 1;
                    break;
                end
            end
            if inner_break
                inner_break = 0;
                break;
            end
        end
        % if we reach this our route hasn't improved, and we break
        outer_break = 1;
    end
    new_route = route;
end

function new_route = two_opt_swap(route, i, k)
    new_route = route(1:i-1);
    new_route = [new_route flip(route(i:k))];
    new_route = [new_route route(k+1:end)];
end
