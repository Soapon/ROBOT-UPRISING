# ROBOT-UPRISING
Rules:
1. Player starts w/ 3 hearts
2. Press Space to shoot
3. WASD or Arrow keys to move
4. Powerup by using the "E" Key
5. When the robot hit the player or reach the right side, the player lose a heart

## What went well
One thing that went better than I expected was coordinating timing in the game. There were a lot of timing parameters, such as enemy spawning and the duration of animations, that required keeping multiple variables flowing naturally. Those systems ultimately worked together smoothly. I was especially proud of how the jump and power-up mechanic functioned, which was highly requested, including the temporary freeze at the top and the destruction of enemies.

## What didn't go well
As the code grew bigger, debugging became harder. The BIGGEST error I ran into that I had trouble with was a bug where the player sprite simply would not appear. To debug this error, I rebuilt the entire code and matched my code to the tutorial line by line to see exactly why the error is happening. Additionally, for my enemy tracking, I tried to rely only on sprite lists as I did for the player, but that made it difficult to track enemy data, so I also created an object list and reconstructed how enemies are being handled.

## What I can do better next time
Next time, I would balance my focus on pure code with earlier consideration of visuals because I went into the coding with the coding architecture in mind but I didn't think about how to transfer that onto the player interface. I spent a lot of time making systems logically sound, which led to issues with spacing and movement once the game was rendered. Prototyping visuals earlier with placeholder assets would help reveal these problems sooner.
