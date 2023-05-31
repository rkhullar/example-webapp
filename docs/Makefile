all: clean build

build:
	@mkdir dist
	@cat medium-article.md | python -m markdown -x fenced_code -x codehilite > dist/body.html
	@pygmentize -S default -f html -a .codehilite > dist/codehilite.css
	echo '<link rel="stylesheet" href="codehilite.css"/>' > dist/header.html
	cat dist/header.html dist/body.html > dist/index.html
	rm dist/header.html dist/body.html

clean:
	@rm -rf dist
