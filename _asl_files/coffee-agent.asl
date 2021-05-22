
cafe_is_open[source("calendar-agent")].
has_some_money.

! get_coffee.


+! get_coffee
    : alice_in_office
    <- goto_office("office");
       ask_for_coffee("coffee").


+! get_coffee
    : not alice_in_office & has_some_money & cafe_is_open
    <- travel_to_cafe("cafe");
       request_favourite_coffee("coffee");
       pay_for_coffee("1");
       + paid_for_coffee;
       return_to_classroom("1");
       + in_class_room.

+! get_coffee
   : not cafe_is_open
   <- scream("aaaaa").









