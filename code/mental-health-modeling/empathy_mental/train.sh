python src/train.py \
	--train_path=../dataset/input-emotional-reactions-reddit.csv \
	--lr=2e-5 \
	--batch_size=32 \
	--lambda_EI=1.0 \
	--lambda_RE=0.5 \
	--save_model \
	--save_model_path=output_emotional/sample2.pth
