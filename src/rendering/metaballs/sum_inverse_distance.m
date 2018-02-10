function f = sum_inverse_distance(x,y,balls)

% Given a ball array of [radius, x0, y0, norm], where x0 and y0 are the
% centre coordinates of the ball, radius of the ball, and specified norm,
% compute the sum of the inverse distances to every ball. The 'distance' in
% question is specified by the norm number. If norm = 1, the L1 norm is
% used, if norm = 2, the euclidean distance is used, and so on for norm =
% 3,4,5 ...

f = 0;
[r,c] = size(balls);

for b = 1:r
    ball = balls(b,:);
    f = f + (ball(1) / norm([x y]-ball(2:3), ball(4)) );
end

end

