cd ..
tar -czf autosnap.tar.gz autosnap-0.1
cp autosnap.tar.gz autosnap-0.1
cd autosnap-0.1

top_path=""

if [ -f "/root/.rpmmacros" ];
then
	config=$(sed -n 1p /root/.rpmmacros)
	top_path=$(echo "$config" | awk '{print $2}')
else
	top_path="/root/rpmbuild/"
fi

echo $top_path

mv autosnap.tar.gz $top_path/SOURCES/

rpmbuild -bb autosnap.spec
