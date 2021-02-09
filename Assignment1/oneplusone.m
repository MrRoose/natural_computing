%% a)
L = 100;
iters = 1500;

p = 1/L;

cur_bitstring = randi(2, L, 1) - 1; % randomly generate bitstring x
fitness_hist = zeros(iters, 1);
fitness_hist(1) = sum(cur_bitstring); 

for i = 2:iters
  probs = rand(L, 1); % for every bit, sample probability of flipping uniformly [0,1]
  candidate_bitstring = cur_bitstring; 
  candidate_bitstring(probs <= p) = abs(candidate_bitstring(probs <= p) - 1);
  candidate_sum = sum(candidate_bitstring);
  if candidate_sum > fitness_hist(i-1)
      cur_bitstring = candidate_bitstring;
      fitness_hist(i) = candidate_sum;
  else 
      fitness_hist(i) = fitness_hist(i-1);
  end
end
figure()
plot(1:iters, fitness_hist)
xlabel("Iterations")
ylabel("Fitness")
title("Simple (1+1)-GA for the Counting Ones problem.")
%% b)

L = 100;
iters = 1500;
runs = 100;

p = 1/L;
max_score = L;
optimum_reached = zeros(runs, 1);
for run = 1:runs
    cur_bitstring = randi(2, L, 1) - 1;
    fitness_hist = zeros(iters, 1);
    fitness_hist(1) = sum(cur_bitstring);
    for i = 2:iters
      probs = rand(L, 1);
      candidate_bitstring = cur_bitstring;
      candidate_bitstring(probs <= p) = abs(candidate_bitstring(probs <= p) - 1);
      candidate_sum = sum(candidate_bitstring);
      if candidate_sum > fitness_hist(i-1)
          cur_bitstring = candidate_bitstring;
          fitness_hist(i) = candidate_sum;
      else 
          fitness_hist(i) = fitness_hist(i-1);
      end
      
    end
    if fitness_hist(iters) == max_score
        optimum_reached(run) = 1;
    end
end
times_optimum_reached = sum(optimum_reached)
%% c)

L = 100;
iters = 1500;
runs = 10;

p = 1/L;
max_score = L;
optimum_reached = zeros(runs, 1);
for run = 1:runs
    cur_bitstring = randi(2, L, 1) - 1;
    fitness_hist = zeros(iters, 1);
    fitness_hist(1) = sum(cur_bitstring);
    for i = 2:iters
      probs = rand(L, 1);
      candidate_bitstring = cur_bitstring;
      candidate_bitstring(probs <= p) = abs(candidate_bitstring(probs <= p) - 1);
      candidate_sum = sum(candidate_bitstring);
      
      cur_bitstring = candidate_bitstring;
      fitness_hist(i) = candidate_sum;
    end
    if fitness_hist(iters) == max_score
        optimum_reached(run) = 1;
    end
end
figure()
plot(1:iters, fitness_hist)
xlabel("Iterations")
ylabel("Fitness")
title("Simple random-GA for the Counting Ones problem.")