. /vol/project/2017/530/g1753002/ocadovenv/ocadovenv/bin/activate

exp_dir=/vol/project/2017/530/g1753002/Feasibility
train_output_dir=$exp_dir/trained_models/tensorflow_trained/random_model_exp
test_file_dir=$exp_dir/test_images/test_ambient

python ./test.py --model_source_dir $train_output_dir --label_path $train_output_dir/output_labels.txt --test_file_dir $test_file_dir --test_result_path $train_output_dir/test_results.pkl --num_test 100
