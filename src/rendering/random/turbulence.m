function [ Turb ] = turbulence( N, D )

size = 2;
Noise = generateNoise(N);
Turb = Noise/(D);
for i = 1:D-1
    Turb = Turb + smoothNoise(Noise,size)/(D-i);
    size = size*2;
end

Turb = Turb/D;

end

