// NAME: CHEAH WENG HOE
// DATE CREATED: 28/1/2025
// LAST MODIFIED: 29/1/2025
// Main JavaScript

$(document).ready(function () {

    eel.init()()

    $('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",
        },
        out: {
            effect: "bounceOut",
        },

    });

    // Siri configuration
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: "1.5",
        speed: "0.11",
        autostart: true
      });

    // Siri message animation
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeInUp",
            sync: true,
        },
        out: {
            effect: "fadeOutUp",
            sync: true,
        },

    });


    // Event to handle Mic Button
    $("#MicBtn").click(function () { 
        eel.play_start_sound()
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.perform_tasks()()
        
    });


    // Event to Handle Shortcut Key
    document.addEventListener('keydown', function (e){
        
        // console.log('Key Pressed: ${e.key}, Meta: ${e.metaKey}, Ctrl: ${e.ctrlKey}, Alt: {e.altKey}');

        if (e.key.toLowerCase() === 'j' && (e.metaKey || e.altKey)) {
            // console.log("Shortcut Triggered!");

            eel.play_start_sound()
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.perform_tasks()()
        }
    });

    function PlayAssistance(message) {
        
        if (message !== "") {

            console.log("Sending to Python:", message); // Debugging log
            eel.perform_tasks(message)();
    
            $("#chatbox").val("");  // Clear input field
            ShowHideButton("");  // Update UI correctly based on input
        }
    }


    // Event to handle hidden buttons
    function ShowHideButton(message) {

        if (message.trim().length === 0) {

            $("#MicBtn").show();
            $("#SendBtn").hide();
        }
        else {

            $("#MicBtn").hide();
            $("#SendBtn").show();
        }
    }

    // Event listener for chatbox input
    $("#chatbox").on("keyup", function () {

        let message = $("#chatbox").val();
        ShowHideButton(message);

    });

    // Event to handle Send Button
    $("#SendBtn").on("click", function () {

        let message = $("#chatbox").val();
        PlayAssistance(message);
        
    });

    // Event listener for Enter key
    $("#chatbox").on("keypress", function (e) {

        if (e.which == 13) {
            let message = $(this).val().trim();
            if (message.length > 0) {
                PlayAssistance(message)
            }
        }
    });

    // Ensure buttons update after Python finishes a task
    eel.expose(updateUI);
    function updateUI() {
        console.log("Updating UI after task completion...");
        let message = $("#chatbox").val();
        ShowHideButton(message); // Ensure correct button visibility
    }


    // Close Eel
    eel.expose(close_window);
    function close_window() {
        window.close(); // Closes the browser window
    }
    
});