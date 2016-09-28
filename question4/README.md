#Challenge Question 4

* The code is in src/question4.py
* Dependencies: To run this code, you will need virtualenv and pip.
  * If on a mac, you can install it by typing:
    ```bash
    sudo easy_install pip
    sudo pip install virtualenv
    ```
* To run the code:
  * Go into the root directory and type:
    ```bash
    virtualenv question4
    ```
  * Go into the question4 directory and type:
    ```bash
    source bin/activate
    ```
 * Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
 * Run the program:
    ```bash
    python src/question4.py
    ```
 * To deactivate virtualenv:
    ```bash
    deactivate
    ```

* How it works:

My thinking behind this program is that a user might be attracted by 
dominant colors in the ad. In this case, the blue elements in the image,
such as the button and the blue headers, are the most attractive.

The program starts by finding the 3 most dominant colors in the image by
using a kmeans clustering algorithm. Once the 3 clusters are identified, 
it looks for the cluster with the darkest color amongst other colors 
that have a a certain amount of saturation. 
Basically, this looks for bright colors that are not white.

After the program finds its target cluster, it starts the reactor. The reactor outputs data every 100
milliseconds for 15 seconds. This data corresponds to coordinates that represent the path of a user's mouse. 
This path basically starts from a random coordinate that is part of our cluster and moves towards other 
target coordinates that are also randomly selected from our cluster. Once the reactor is finished outputting 
data, the program shows an image representation of those paths.
