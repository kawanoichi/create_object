help:
	@echo Dockerセットアップ
	@echo "$$ make docker-setup"
	
	@echo Dockerセットアップ
	@echo "$$ make permission"
	
	@echo Docker起動
	@echo "$$ make docker-start"
	
	@echo Docker終了
	@echo "$$ make docker-stop"
	
	@echo Uploadした画像の削除
	@echo "$$ make rm"


docker-setup:
	sudo chmod -R 777 create_object
	sudo chown -R www-data:www-data create_object 
	sudo docker build -t create_object .
	docker run -d --name create_object -p 8000:80 -v ~/create_object/create_object:/var/www/html create_object
	
# 新しいファイルを作成した場合に使用する
permission:	
	sudo chmod -R 777 create_object
	sudo chown -R www-data:www-data create_object 

docker-terminal:
	docker exec -i -t create_object bash

docker-start:
	docker start create_object

docker-stop:
	docker stop create_object

rm:
	rm -rf ~/create_object/create_object/storage/app/public/image_data/*.png

push:
	git add .
	git commit -m "update"
	git push origin main