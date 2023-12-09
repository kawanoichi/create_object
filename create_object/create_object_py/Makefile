help:
	@echo 3Dオブジェクト生成ツールを実行する
	@echo "$$ make run"
	@echo 画像から点群生成
	@echo "$$ make predict"
	@echo 点群に表面情報を生成
	@echo "$$ make surface"
	@echo 権限を許可する
	@echo "$$ make permission"
	@echo 全てのソースコードをフォーマットする
	@echo "$$ make format"

run:
	poetry run python3 -m src airplane.png

predict:
	poetry run python3 src/predict_point_cpu.py

surface:
	poetry run python3 src/create_surface.py

permission:	
	chmod -R 777 *
	chown -R www-data:www-data * 

format:
	poetry run python3 -m autopep8 -i -r src/ tests/

zikken:
	python3 src/read_image.py