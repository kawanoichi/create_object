help:
	@echo 3Dオブジェクト生成ツールを実行する
	@echo "$$ make run"
	@echo 点群に表面情報を生成
	@echo "$$ make surface"
	@echo 権限を許可する
	@echo "$$ make permission"
	@echo 全てのソースコードをフォーマットする
	@echo "$$ make format"
	@echo 全てのソースコードをフォーマットする
	@echo "$$ make rm"
	@echo "$$ make npy_rm"

run:
	python3 -m src airplane.png

surface:
	poetry run python3 src/create_surface.py

permission:	
	chmod -R 777 *
	chown -R www-data:www-data * 

format:
	python3 -m autopep8 -i -r src/ tests/

rm:
	find data/ -maxdepth 1 -type f \( -not -name 'airplane.png' -and -not -name '*.npy' -and -not -name '*.pth' \) -delete

npy_rm:
	rm data/predict_points/*/*.npy