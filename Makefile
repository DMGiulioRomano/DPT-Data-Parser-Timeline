.PHONY: test clean


test:
	mkdir -p build
	cd build && cmake ..
	cd build && cmake --build .
	cd build && ctest --output-on-failure 
clean:
	sudo rm -rf build