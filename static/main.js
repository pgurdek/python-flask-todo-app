    function show_alert(event) {
        event.preventDefault();
        if (confirm("Do you really want to do this?")){
            document.forms[0].submit();
            }
        else{
            return false;
        }

    }/**
 * Created by pgurdek on 05.03.17.
 */
