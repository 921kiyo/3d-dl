function [ T ] = turbulent_rgb( N )
%TURBULENT_RGB Summary of this function goes here
%   Detailed explanation goes here

min_depth = 2;
max_depth = 6;

T = zeros(N,N,3);
T(:,:,1) = turbulence(N,randi([min_depth max_depth]));
T(:,:,2) = turbulence(N,randi([min_depth max_depth]));
T(:,:,3) = turbulence(N,randi([min_depth max_depth]));

end

