console.log("Loading function");
var AWS = require("aws-sdk");

exports.handler = function(event, context) {
    event["responseLink"] = "https://guarded-lowlands-96300.herokuapp.com/solicit-review?senderId=" + event["senderId"] + "&candy=" + escape(event["choice"]);
    var eventText = JSON.stringify(event, null, 2);
    console.log("Received event:", eventText);
    var sns = new AWS.SNS();
    var params = {
        Message: eventText, 
        Subject: "Candy Choice",
        TopicArn: "arn:aws:sns:us-east-1:774013277495:hackathon-team-scrub-notifications"
    };
    sns.publish(params, context.done);
};