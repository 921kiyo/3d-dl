. /vol/project/2017/530/g1753002/ocadovenv/ocadovenv/bin/activate
exp_dir=/data/g1753002_ocado
image_dir=$exp_dir/final_zip/ten_set_model_official_SUN_back_2018-04-07_13_19_16/images
output_dir=/data/who11/ocado_desperation_logs
python ./retrain.py --image_dir $image_dir --output_dir $output_dir --how_many_training_steps 8000 --eval_step_interval 20
