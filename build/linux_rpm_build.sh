#!/bin/bash
../venv/bin/pyinstaller savings.spec
mv dist/savings dist/opt/
rm target/savings.rpm
fpm -s dir --log error --rpm-rpmbuild-define "_build_id_links none" -C dist -n savings -v 1.0 --vendor lukasszz -t rpm -p target/savings.rpm
