all: clean setup style overview.html part-1-platforms-and-resource-prep.html part-2-project-setup-and-local-development.html part-3-deploying-to-api-gateway-and-lambda.html post

clean:
	@rm -rf dist

post:
	@rm dist/header.html

setup:
	@mkdir -p dist
	@ln -s `pwd`/images dist/images

style:
	@pygmentize -S default -f html -a .codehilite > dist/codehilite.css
	@echo '<link rel="stylesheet" href="codehilite.css"/>' > dist/header.html

%.html: %.md
	@mkdir -p dist
	@cat $< links.md > dist/$@-linked.md
	@cat dist/$@-linked.md | python -m markdown -x fenced_code -x codehilite > dist/$@.body
	@cat dist/header.html dist/$@.body > dist/$@
	@rm dist/$@.body dist/$@-linked.md

%.md:
