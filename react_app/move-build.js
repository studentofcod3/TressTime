// Move the build from the current app into the django-app, overwriting any pre-existing build.

const fs = require('fs-extra');
const path = require('path');

const sourceDir = path.join(__dirname, 'build')
const destinationDir = path.resolve(__dirname, '../django_app/frontend/static/frontend/build')

fs.move(sourceDir, destinationDir, { overwrite: true }, function (err){
    if (err) {
        return console.error(err);
    }
    console.log('Build directory moved successfully');
});