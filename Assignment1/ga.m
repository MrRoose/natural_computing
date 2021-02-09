function [final_population, best_fitness_hist, times] = ga(cities, n_iters, memetic, p_elitism, p_c, p_m, population_size)
%GA Summary of this function goes here
%   Detailed explanation goes here
    iters = n_iters;
  

    
    deterministic_tournament_selection = 1; % always pick best tournament participant

    n_cities = length(cities);

    tic;
    
    % generate population
    population = zeros(population_size, n_cities);
    for i = 1:population_size
        initial_route = randperm(n_cities); % random permutation of 1:n_cities
        if memetic
            population(i, :) = local_search(initial_route, cities);
        else
            population(i, :) = initial_route;
        end
    end

    % assign fitness scores to population
    population_fitness = calc_population_fitness(population, cities);
    
    k = 2; % binary tournament selection: we have two tournaments with k=2 to select two parents

    n_elitism = round(p_elitism * population_size);
    n_elitism = n_elitism + mod(n_elitism, 2); % make sure n_elitism is even

    best_fitness_hist = zeros(iters, 1);
    times = zeros(iters, 1); % keep track of running time (for fair comparison)
    
    
    for iter = 1:iters
        mutation_pool = tournament_selection(k, deterministic_tournament_selection, population, population_fitness, n_elitism);
        new_population = zeros(size(population));
        new_population(1:n_elitism, :) = mutation_pool(1:n_elitism, :);

        for i = n_elitism+1:2:population_size
            % Pick two parents from our pool
            parent_ids = randi(population_size, 2, 1);
            parents = mutation_pool(parent_ids, :);
            if rand() <= p_c
                new_population(i:i+1, :) = order_crossover_1(parents);
            else
                new_population(i:i+1, :) = parents;
            end       
        end

        for i = 1:population_size
            if rand() < p_m
                new_population(i, :) = rsm(new_population(i, :));
            end
        end
        
        if memetic
            % local search
            for i = 1:population_size
                new_population(i, :) = local_search(new_population(i, :), cities);
            end
        end

        population = new_population;
        population_fitness = calc_population_fitness(population, cities);
        best_fitness_hist(iter) = min(population_fitness);
        times(iter) = toc;
    end
    final_population = population;
end

%% Functions

function fitness = calc_population_fitness(population, cities)
    population_size = size(population, 1);
    fitness = zeros(population_size, 1);
    for i = 1:population_size
        fitness(i) = calc_dist(population(i, :), cities);
    end
end

function dist = calc_dist(route, cities)
    dist = 0;
    for i = 1:length(route)-1
        city_1 = route(i);
        city_2 = route(i+1);
        dist = dist + sqrt(sum((cities(city_1,:) - cities(city_2,:)).^2));
    end
end

function mutation_pool = tournament_selection(k, deterministic, population, population_fitness, n_elitism)
    % n_elitism has to be even
    population_size = length(population_fitness);
    mutation_pool_ids = zeros(population_size,1);
    
    [~, sorted_fitness_idxs] = sort(population_fitness);
    mutation_pool_ids(1:n_elitism) = sorted_fitness_idxs(1:n_elitism);
    
    for i = n_elitism+1:population_size
        % pick two random indices
        tournament_ids = randi(population_size, 1, k);
        tournament_probs = population_fitness(tournament_ids)/sum(population_fitness(tournament_ids));
        if deterministic
            [~, winner_id] = max(tournament_probs);
        else
            winner_id = randsrc(1,1,[tournament_ids; tournament_probs']);
        end
        mutation_pool_ids(i) = winner_id;
    end
    
    % fill mating_pool
    mutation_pool = population(mutation_pool_ids, :);
end

function offspring = order_crossover_1(parents)
% Order crossover where we start from the second cutpoint
    length_parents = size(parents, 2);
    cut_points = sort(randi(length_parents, 2, 1));
    
    offspring = zeros(size(parents));
    offspring(:, cut_points(1):cut_points(2)) = parents(:, cut_points(1):cut_points(2));
    
    missing_cities_1 = [parents(2, cut_points(2)+1:end),  parents(2, 1:max(cut_points(2),1))]; % right order
    missing_cities_2 = [parents(1, cut_points(2)+1:end),  parents(1, 1:max(cut_points(2),1))];

    missing_cities_1 = missing_cities_1(~ismember(missing_cities_1, offspring(1,:))); % remove cities already there
    missing_cities_2 = missing_cities_2(~ismember(missing_cities_2, offspring(2,:)));

    missing_cities = [missing_cities_1; missing_cities_2];
    missing_cities = circshift(missing_cities, cut_points(1)-1, 2);
    offspring(offspring == 0) = missing_cities;   
end

function mutation = rsm(route)
    cut_points = sort(randi(length(route), 2, 1));
    sequence = cut_points(1):cut_points(2);
    mutation = route;
    mutation(sequence) = mutation(flip(sequence));
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