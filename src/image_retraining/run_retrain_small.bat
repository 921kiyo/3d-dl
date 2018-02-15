. /vol/project/2017/530/g1753002/ocadovenv/ocadovenv/bin/activate
exp_dir=/vol/project/2017/530/g1753002/Feasibility
image_dir=$exp_dir/mvp_training_data_correct/white/
output_dir=$exp_dir/trained_models/tensorflow_trained/white_model_exp
python ./retrain.py --image_dir $image_dir --output_dir $output_dir --how_many_training_steps 500
