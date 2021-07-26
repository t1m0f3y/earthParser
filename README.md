# earthParser

## Only for Educational purposes

The project is aimed to get the geographical data from web pages (like google maps, yandex maps, OSM, etc.).

For now, I'm only trying to get the elevation for particular lon lat values.

The Selenium webdriver is used (for Chrome).
Capabilities for 'elevationParser_votetovid.py':
  1. Get the elevation data with 0.001 step size (around 60 meters) for predefined area (rectangle);
  2. There are a lot of '?' signs for some coordinates. It should be interpolated for more accuracy;
  3. The file structure: 'Lon Lat Elevation';

TODO:
  1. Get the buildings height;
  2. Understand is it a building or something else at particular coordinates;
  3. Visualize the surface (with 3D plot\OpenGL\DirectX\etc);
  4. Avoid 'time.sleep()' method. Need some "waiting system" for requests.

  
