function centroids = kmeans(data, k)
    
    [N, D] = size(data);

    assignments = zeros(N, 1);
    
    % We initialize using data points
   
    starting_idxs = randsample(N, k); 
    centroids = data(starting_idxs, :);
    
    keep_going = 1;
    while keep_going
        dists = zeros(N, k);
       
        for i = 1:k
            dists(:, i) = sqrt(sum((data - centroids(i, :)).^2, 2));
        end

        [min_dists, new_assignments] = min(dists, [], 2);
        
        keep_going = sum(assignments == new_assignments) ~= N;
        
        for i = 1:k
            centroids(i, :) = mean(data(new_assignments == i, :));
        end
        assignments = new_assignments;
    end
end