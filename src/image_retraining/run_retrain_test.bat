. /vol/project/2017/530/g1753002/ocadovenv/ocadovenv/bin/activate

exp_dir=/data/g1753002_ocado
train_output_dir=/data/who11/ocado_desperation_logs
test_file_dir=$exp_dir/images_proc_test_and_validation

python ./tf_eval.py --model_source_dir $train_output_dir --label_path $train_output_dir/output_labels.txt --test_file_dir $test_file_dir --test_result_path $train_output_dir/test_results.pkl --num_test 160
