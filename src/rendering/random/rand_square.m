function [ Sq ] = rand_square( L )

    maxval = 1.0;

    Sq = zeros(L,L);
    assert(L>0, "L needs to be positive!");
    Sq(1,1) = rand * maxval;
    
    for i = 2:L
        
        Sq(i,1) = rand_step([Sq(i-1,1)],0,maxval);
        for j = 2:1:i-1
            Sq(i,j) = rand_step([Sq(i,j-1) Sq(i-1,j)],0,maxval);
        end
        Sq(i,i) = rand_step([Sq(i,i-1)],0,maxval);
        for k = i-1:-1:1
            Sq(k,i) = rand_step([Sq(k+1,i) Sq(k,i-1)],0,maxval);
        end
        
    end

end

function [n] = rand_step(input_arr, minval, maxval)
    max_step = 0.3*(maxval-minval);
    mu = mean(input_arr);
    %step = rand*2*max_step - max_step;
    step = normrnd(0,max_step);
    
    n = mu + step;
    n = max(minval,n);
    n = min(maxval,n);
end