function [filled] = metaball(image_rows, image_cols, balls, thres)

% Given number of elements in image rows and columns, a list of balls
% [[radius, x0, y0, norm]], and a threashold value, create metaballs from
% the specified parameters
% outputs: an image array of ones and zeros, where pixels with ones
% correspond to the inside of the metaballs

filled = zeros(image_rows,image_cols);

for r = 1:image_rows
    for c = 1:image_cols
        
        % compute sum inverse distance from each pixel
        f = sum_inverse_distance(r,c,balls);
        
        % if more than threshold, fill image pixel
        if (f>thres)
            filled(r,c) = 1;
        end
        
    end
end

end

