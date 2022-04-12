<!-- Add banner here -->
![Banner](/readme-editor/banner.png)

# MSC - Building AI Controllers for the Game of Carcacassonne
Master's Project - Carcassonne, AI, MCTS, Expectimax

<!-- Add buttons here -->

<!-- Describe your project in brief -->

The main idea behind the thesis is building and testing AI controllers to play the famous euro-style board game of Carcassonne. AI algorithms include Monte Carlo Tree Search (MCTS), MCTS with Rapid Actio Value Estimation (MCTS-RAVE) and Minimax search algorithms. Some controllers incorporate evolutionary algorithms, in paarticular Evolutionary Strategies (ES) to improve the decision making processes of these AI algorthims.

Extra features include an interactive Game UI that allows human players to compete against AI controllers


# Demo-Preview

<!-- Add a demo for your project -->

<!-- After you have written about your project, it is a good idea to have a demo/preview(**video/gif/screenshots** are good options) of your project so that people can know what to expect in your project. You could also add the demo in the previous section with the product description. -->
Game UI:

<!-- [menu](/readme-editor/menu.gif) -->
![pygame](/readme-editor/pygame.gif)

Controls:
* Arrows - Rotate tile (Left & Right)
* NumKeys - Placement of Meeple, if available. (Numbers seen in menu on right as well as on the tile image)
* Click - Place tile one of the available positions
* Spacebar - Make AI controller to choose move

Square Colours:
* Green - Available position on board
* Blue - Available position on board, but **not** for that Meeple choice


# Table of contents

- [Project Title](#project-title)
- [Demo-Preview](#demo-preview)
- [Table of contents](#table-of-contents)
- [Packages Required](#packages-required)
- [Usage](#usage)
    - [Experiments](#experiments)
    - [Results UI](#results-ui)
    - [Game UI](#game-ui)
- [Development](#development)
- [Footer](#footer)

# Installation
[(Back to top)](#table-of-contents)

* Clone the project
* Go to project folder
* Unzip the `logs.zip` file, and then delete `logs.zip`
* Install all packages in `requirements.txt`:

```
pip install -r requirements.txt
```


# Usage
[(Back to top)](#table-of-contents)


### Experiments
[(Back to top)](#table-of-contents)

To replicate the results from any of the experiments, just execute any of the python scripts with prefix of `Experiment_...`. Results and logs of each experiment are stored within their own folder within the `.../logs` directory.

Example:

* Run script:

```
python Experiment_SAMPLE.py
```
* Location of log files:

```
.../Carcassonne/logs/Experiment_SAMPLE_1_2021-07-18
```

### Results UI
[(Back to top)](#table-of-contents)

Run the app script (`python Plotly_App.py`) and the following message should appear:

> Dash is running on **http://127.0.0.1:8050/**</br>
> * Serving Flask app "Plotly_App" (lazy loading)
> * Environment: production
>   WARNING: This is a development server. Do not use it in a production deployment.
>   Use a production WSGI server instead.
> * Debug mode: on

Copy and paste the url (hyperlink) into a browser to access the UI containing statistical results from the experiments. A page (similar to below) should appear.

![results_ui](/readme-editor/results_ui.PNG)

Use the dropdowns available to filter through the different results sets and filter by AI controller. All plots are **interactive** and will display extra information when hovered over. UI will remain online as long as the `Plotly_App.py` is running. 

The results from each of the experiments will be numbered with how they appear in the report. For example, the results for the first experiment will be listed as `1_EXP_MCTS_Param` in the first dropdown menu on the left-hand side.

The second dropdown is to add the statistics from particular controllers (available in the dropdown) to the figures and tables in the dashboard. The third dropdown is specifically to choose which MCTS-ES controllers' stats to view. 


### Game UI
[(Back to top)](#table-of-contents)

Run the following bash script from the command line to activate the Carcassonne game UI:

```
bash ./PLAY_GAME_UI.sh
```

Then a menu will pop up. Click on the **arrows** to choose Player 1 and Player 2. Click `Play` to start the game. The game UI (seen above), powered by `pygame` will pop-up next.
