function [img] = random_metaball(image_row, image_col, n_balls, size)

% Given number of balls, and an image size, generate random metaballs in
% the image

% distribution of the centroid of the metaballs
centre_x_range = [1 image_row];
centre_y_range = [1 image_col];

% distribution of each ball from centroid (10% of image size gives a good
% variation of shapes)
sigma_x = round(image_row/10);
sigma_y = round(image_col/10);

% the radius distribution of each ball is proportional to the image
% size times a constant, and inversely proportional to number of balls.
% This should keep the distribution of the size of the blob fairly
% constant
min_ball_radius = round(image_col/(15*n_balls));
max_ball_radius = round(image_col/(10*n_balls));

centre_x = randi(centre_x_range, 1);
centre_y = randi(centre_y_range, 1);

% ball array
ball = zeros(n_balls,4);

% generate each ball
for i = 1:n_balls
    % x,y centre of ball
    x = round( normrnd( centre_x, sigma_x, 1, 1) );
    y = round( normrnd( centre_y, sigma_y, 1, 1) );
    x = min(max(x,1),image_row); % out-of bounds check
    y = min(max(y,1),image_row); % out-of bounds check

    % get radius
    r = randi( [min_ball_radius, max_ball_radius], 1);
    
    % random power norm for inverse distance
    p = randi([1 3],1);

    ball(i,:) = [ r x y p ];
end

img = metaball(image_row, image_col , ball, size);

end

