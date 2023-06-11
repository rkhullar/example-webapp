all: clean style overview.html part-1-platforms-and-resource-prep.html part-2-project-setup-and-local-development.html part-3-deployment.html post

clean:
	@rm -rf dist

post:
	@rm dist/header.html

style:
	@mkdir -p dist
	@pygmentize -S default -f html -a .codehilite > dist/codehilite.css
	@echo '<link rel="stylesheet" href="codehilite.css"/>' > dist/header.html

%.html: %.md
	@mkdir -p dist
	@cat $< | python -m markdown -x fenced_code -x codehilite > dist/$@.body
	@cat dist/header.html dist/$@.body > dist/$@
	@rm dist/$@.body

%.md:
