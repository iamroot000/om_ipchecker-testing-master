HUB='omdockerhub.neweb.me'
ct_name=${1}
image_name="${ct_name}"
CT=`docker inspect --format="{{.Id}}" ${ct_name}`
echo -en "Commiting image please wait....\n"
docker login -u omadmin -p "Ad@sn1407" omdockerhub.neweb.me:5000
	docker export ${CT} | docker import - ${HUB}:5000/${image_name}-${2}

