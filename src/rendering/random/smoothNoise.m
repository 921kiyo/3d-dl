function [ smoothed ] = smoothNoise( noise, scale )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

    [R,C] = size(noise);
    smoothed_X = zeros(R,C);
    smoothed_Y = zeros(R,C);
    for j=1:C
        smoothed_X(:,j) = j/scale;
    end
    for i = 1:R
        smoothed_Y(i,:) = i/scale;
    end

    smoothed = interp2(noise, smoothed_X+1, smoothed_Y+1);
end
