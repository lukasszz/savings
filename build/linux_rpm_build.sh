#!/bin/bash
rm -R build
rm -R dist/opt/*
rm -R dist/savings
rm target/savings.rpm


../venv/bin/pyinstaller savings.spec

mv dist/savings dist/opt/

fpm -s dir --log error --rpm-rpmbuild-define "_build_id_links none" -C dist -n savings -v 1.1.0 --vendor lukasszz -t rpm -p target/savings.rpm
