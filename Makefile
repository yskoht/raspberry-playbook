VARS_FILE := vars.yml

vars_file_exists = $(shell ls | grep ${VARS_FILE})
ifeq (${vars_file_exists}, ${VARS_FILE})
	opt = --extra-vars "@$(VARS_FILE)" --ask-vault-pass
endif

.PHONY: encrypt
encrypt:
	ansible-vault encrypt vars.yml

.PHONY: decrypt
decrypt:
	ansible-vault decrypt vars.yml

.PHONY: create-sd
create-sd:
	ansible-playbook -i hosts create-sd.yml --ask-become-pass

.PHONY: configure
configure:
	ansible-playbook -i hosts configure.yml $(opt)

.PHONY: setup-dev
setup-dev:
	ansible-playbook -i hosts setup-dev.yml

.PHONY: setup-timelapse
setup-timelapse:
	ansible-playbook -i hosts setup-timelapse.yml $(opt)

.PHONY: setup-epaper
setup-epaper:
	ansible-playbook -i hosts setup-epaper.yml $(opt)
