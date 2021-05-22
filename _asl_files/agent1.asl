! count.

alice[source("we")].

+! count
    : inverted
    <-  + has_cat;
        .count_down(3);
       - inverted.


+! count
    : not inverted & is_in_spain
    <-  + inverted; .print("Qqa"); .count_up(3).


+! count
    : not inverted & not is_in_spain | not has_cat | not has_spinach
    <-  + inverted; .print("Counting up.."); .count_up(3).

+ hello(Message)
    : true
    <- .print(Message).

