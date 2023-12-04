help:
	@echo Dockerセットアップ
	@echo "$$ make docker-setup"
	
	@echo Dockerセットアップ
	@echo "$$ make permission"
	
	@echo Docker起動
	@echo "$$ docker-start"
	
	@echo Docker終了
	@echo "$$ docker-stop"


docker-setup:
	sudo chmod -R 777 create_object
	sudo chown -R www-data:www-data create_object 
	sudo docker build -t create_object .
	docker run -d --name create_object -p 8000:80 -v ~/create_object/create_object:/var/www/html create_object
	
# 新しいファイルを作成した場合に使用する
permission:	
	sudo chmod -R 777 create_object
	sudo chown -R www-data:www-data create_object 

docker-start:
	docker start create_object

docker-stop:
	docker stop create_object
