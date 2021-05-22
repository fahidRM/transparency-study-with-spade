

! count.


+! count
    : inverted
    <-  + has_cat;
        .count_down(3).
       //- inverted.
       //.send("agent2@localhost", achieve, hello("Hello World!"));
       //! count.
       //.


+! count
    : not inverted
    <- .send("agent1@localhost", tell, "jjp");
       .count_up(3);
       + inverted;
       ! count.

+ hello(Message)
    : true
    <- .print(Message).

