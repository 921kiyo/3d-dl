# activate CUDA
create a file in your home directory called .bash_profile

with content and save:

```
if [ -f /vol/cuda/8.0.61-cudnn.7.0.2/setup.sh ]
then
   . /vol/cuda/8.0.61-cudnn.7.0.2/setup.sh
fi
```

then log out and log in again
