#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     To make the game Blackjack
#
# Author:      wissc9564
#
# Created:     08/10/2013
# Copyright:   (c) wissc9564 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
from random import*
from graphics import*
from time import*

#Calls the games functions
def main():
    money = 1000
    #creates the infile and outfile where the high scores will be saved
    infile = open("highscores.txt", "r")
    outfile = open("highscores.txt", "a")
    #initiates the list that the scores will be stored in
    highscorelist = []

    #creates a list out of the scores from previous games and sorts them and assigns the highest previous score to the highscore variable
    for line in infile:
        s = str(line.split())
        s = s.replace("[","").replace("'","").replace("]","").replace(",","")
        s = int(s)
        highscorelist.append(s)
    highscorelist.sort()

    highscore = str((highscorelist[len(highscorelist)-1]))

    #infinite loop so the bank stays the same until you quit
    while True:
        splithandcounter = 0
        #initiates the list that will be used to store the cards that have been dealt
        used = []
        win,rectangle2,rectangle9 = MakeLayout()
        splitchoice = "no"

        #draws the high score on the top of the window
        highscorewin = Text(Point(575,20),"High Score: ${0}".format(highscore))
        highscorewin.setTextColor('white')
        highscorewin.setSize(14)
        highscorewin.draw(win)

        betbox,balance,startbutton = BetLayout(win,money)
        bet,money,pot = makeABet(win,betbox,balance,startbutton,money)
        dealercard1,dealercard2,dealervalue,graphdealer1,graphdealer2,used,dealersplit = FirstTwoCards(used)

        #creates text in the box that shows the dealers current value
        dealervaluegraph = Text(Point(39.5,100),dealervalue-dealercard1)
        dealervaluegraph.draw(win)

        playercard1,playercard2,playervalue,graphplayer1,graphplayer2,used,splitoption = FirstTwoCards(used)
        #creates the text in the box that shows the players current value
        playervaluegraph = Text(Point(39.5,400),playervalue)
        playervaluegraph.draw(win)

        secondplayer = graphFirstTwo(win,graphdealer1,graphdealer2,graphplayer1,graphplayer2)

        winner,money = checkWinnerFirstTwoCards(dealervalue,playervalue,win,graphdealer1,dealervaluegraph,money,bet,dealercard2)

        #if the player gets blackjack on the first two cards, they win
        if winner == "Player":
            finalplayervalue = playercard1 + playercard2
            finaldealervalue = dealercard1 + dealercard2
            balance.setText("${0}".format(money))
            doubledownhand1 = "no"
            compare(win,finalplayervalue,finaldealervalue,playercard1,playercard2,balance,bet,money,doubledownhand1)
            playagain(win)

        else:
            #asks for insurance if the dealers face up card is an ace
            if dealercard2 == 11 and (money - int(bet)/2) > 0:
                money,balance,insuranceanswer,insurancevalue = insurance(win,bet,money,balance)
            else:
                insuranceanswer = "none"

            if winner == "Dealer":
                finalplayervalue = playercard1 + playercard2
                finaldealervalue = dealercard1 + dealercard2
                dealervaluegraph.setText(dealercard1+dealercard2)
                doubledownhand1 = "no"
                compare(win,finalplayervalue,finaldealervalue,playercard1,playercard2,balance,bet,money,doubledownhand1)
                if insuranceanswer == "yes":
                    balance.setText("${0}".format(money+2*insurancevalue))
                sleep(1)
                dealerflip = Image(Point(125,100),graphdealer1 + ".gif")
                dealerflip.draw(win)
                playagain(win)
            #if the player doesnt get blackjack on the first two cards, the game will proceed
            else:
                if splitoption == "yes" and money - int(bet) >= 0:
                    splitchoice,hand1value,hand2value,doubledownhand1,doubledownhand2,money = splitting(win,bet,money,balance,playervaluegraph,playervalue,playercard1,playercard2,secondplayer,pot,rectangle2,rectangle9,used)


                if splitchoice == "no":
                    #asks for double down
                    if money - int(bet) >= 0:
                        doubledownhand1,doubledownhand2 = DoubleDown(win,splitchoice)
                        if doubledownhand1 == "yes":
                            pot.setText("${0}".format(int(bet)*2))
                            money = money - int(bet)
                            balance.setText("${0}".format(money))
                    #calls player function if player did not click yes on splitting
                    else:
                        doubledownhand1 = "no"
                    cards,suits,finalplayervalue = Player(win,playervalue,dealervalue,playervaluegraph,playercard1,playercard2,used,splitoption,splithandcounter,doubledownhand1)
                elif splitchoice == "yes":
                    finalplayervalue = hand1value
                finaldealervalue,used = Dealer(win,dealervalue,dealervaluegraph,dealercard1,dealercard2,finalplayervalue,used,graphdealer1,splitchoice)
                #calls compare/splitcompare depending on if the player split
                if splitchoice == "no":
                    money = compare(win,finalplayervalue,finaldealervalue,playercard1,playercard2,balance,bet,money,doubledownhand1)
                else:
                    splitCompare(win,hand1value,hand2value,finaldealervalue,balance,bet,money,doubledownhand1,doubledownhand2)
                playagain(win)

        #infinite loop that gets the users click that will only break when the user clicks quit or play again
        while True:
            endclick = win.getMouse()
            endx = endclick.getX()
            endy = endclick.getY()

            #clicks on play again
            if endx >= 1000 and endx <= 1125 and endy >= 190 and endy <= 240:
                win.close()
                break
            #clicks on quit
            elif endx >= 1000 and endx <= 1125 and endy >= 260 and endy <= 310:
                #adds the score to the outfile with previous scores to be checked for highscore at the start of a new game
                if len(highscorelist) == 1:
                    print("",file = outfile)
                    print(money,file = outfile)
                else:
                    print(money,file = outfile)
                win.close()
                sys.exit()
            #nothing happens if they click outside of a button
            else:
                pass


#compares the final values and pays out accordingly if the user chose to split their cards
def splitCompare(win,hand1value,hand2value,finaldealervalue,balance,bet,money,doubledownhand1,doubledownhand2):

    #both hands win
    if (hand1value > finaldealervalue and hand1value <= 21 and hand2value > finaldealervalue and hand2value <= 21) or (hand1value <= 21 and hand2value <= 21 and finaldealervalue > 21):
        #double down variations
        if doubledownhand1 == "yes" and doubledownhand2 == "yes":
            money = money + int(bet)*4 + int(bet)*4
        elif doubledownhand1 == "yes" and doubledownhand2 == "no":
            money = money + int(bet)*4 + int(bet)*2
        elif doubledownhand1 == "no" and doubledownhand2 == "yes":
            money = money + int(bet)*2 + int(bet)*4
        elif doubledownhand1 == "no" and doubledownhand2 == "no":
            money = money + int(bet) + int(bet)

        balance.setText("${0}".format(money))

    #hand 1 wins
    elif (hand1value > finaldealervalue and hand1value <= 21 and hand2value < finaldealervalue) or (hand1value <= 21 and hand1value > finaldealervalue and hand2value > 21) or (hand1value <= 21 and hand2value > 21 and finaldealervalue > 21):
        #double down variations
        if doubledownhand1 == "yes" and doubledownhand2 == "yes":
            money = money + int(bet)*4
        elif doubledownhand1 == "yes" and doubledownhand2 == "no":
            money = money + int(bet)*4
        elif doubledownhand1 == "no" and doubledownhand2 == "yes":
            money = money + int(bet)*2
        balance.setText("${0}".format(money))

    #hand 2 wins
    elif (hand2value > finaldealervalue and hand2value <= 21 and hand1value < finaldealervalue) or (hand2value <= 21 and hand2value > finaldealervalue and hand1value > 21) or (hand2value <= 21 and hand1value > 21 and finaldealervalue > 21):
        #double down variations
        if doubledownhand1 == "yes" and doubledownhand2 == "yes":
            money = money + int(bet)*4
        elif doubledownhand1 == "yes" and doubledownhand2 == "no":
            money = money + int(bet)*2
        elif doubledownhand1 == "no" and doubledownhand2 == "yes":
            money = money + int(bet)*4
        balance.setText("${0}".format(money))

    #both hands lose
    elif (hand1value < finaldealervalue and hand2value < finaldealervalue) or (hand1value > 21 and hand2value > 21 and finaldealervalue <= 21):
        balance.setText("${0}".format(money))

    return money



#Allows the user to double their initial bet, either on 1 hand or a split 2 hands
def DoubleDown(win,splitchoice):
    #creates the text that asks for double down and the buttons
    DoubledownText = Text(Point(862.5,250),"Double Down\nHand 1?")
    DoubledownText.setSize(24)
    DoubledownText.setTextColor('white')
    DoubledownText.draw(win)

    yesDD = Rectangle(Point(1000,190),Point(1125,240))
    yesDD.setFill("limegreen")
    yesDD.draw(win)

    noDD = Rectangle(Point(1000,260),Point(1125,310))
    noDD.setFill('firebrick')
    noDD.draw(win)

    yestext = Text(Point(1062.5,215),"YES")
    yestext.setSize(16)
    yestext.draw(win)

    notext = Text(Point(1062.5,285),"NO")
    notext.setSize(16)
    notext.draw(win)

    #gets the users click to see if they want to double down
    while True:
        DDClick1 = win.getMouse()
        DDClick1X = DDClick1.getX()
        DDClick1Y = DDClick1.getY()

        #clicks on yes
        if DDClick1X >= 1000 and DDClick1X <= 1125 and DDClick1Y >= 190 and DDClick1Y <= 240:
            doubledownhand1 = "yes"
            break

        #clicks on no
        elif DDClick1X >= 1000 and DDClick1X <= 1125 and DDClick1Y >= 260 and DDClick1Y <= 310:
            doubledownhand1 = "no"
            break

        else:
            pass
    #if the user split, it will also ask if the user wants to double down the second hand
    if splitchoice == "yes":
        DoubledownText.setText("Double Down\nHand 2?")

        while True:
            DDClick2 = win.getMouse()
            DDClick2X = DDClick2.getX()
            DDClick2Y = DDClick2.getY()

            #clicks on yes
            if DDClick2X >= 1000 and DDClick2X <= 1125 and DDClick2Y >= 190 and DDClick2Y <= 240:
                doubledownhand2 = "yes"
                break

            #clicks on no
            elif DDClick2X >= 1000 and DDClick2X <= 1125 and DDClick2Y >= 260 and DDClick2Y <= 310:
                doubledownhand2 = "no"
                break

            else:
                pass
    else:
        doubledownhand2 = "no"

    DoubledownText.undraw()
    yesDD.undraw()
    noDD.undraw()
    yestext.undraw()
    notext.undraw()

    return doubledownhand1,doubledownhand2


#A function that allows the user to split their hand into 2 separate hands if the first two cards are the same face value
def splitting(win,bet,money,balance,playerscore,playervalue,playercard1,playercard2,secondplayer,pot,rectangle2,rectangle9,used):
    #initiates the card counter for each hand (used to draw the cards onto the window)
    hand1cardcounter = 1
    hand2cardcounter = 1
    cards = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    suits = ["d","h","s","c"]
    #creates the text and buttons asking the user if they want to split
    splittext = Text(Point(850,250),"Split?")
    splittext.setTextColor('white')
    splittext.setSize(20)
    splittext.draw(win)

    yessplit = Rectangle(Point(1000,190),Point(1125,240))
    yessplit.setFill("limegreen")
    yessplit.draw(win)

    nosplit = Rectangle(Point(1000,260),Point(1125,310))
    nosplit.setFill('firebrick')
    nosplit.draw(win)

    yestext = Text(Point(1062.5,215),"YES")
    yestext.setSize(16)
    yestext.draw(win)

    notext = Text(Point(1062.5,285),"NO")
    notext.setSize(16)
    notext.draw(win)

    splithandcounter = 1


    #infinite loop that gets the users click that breaks when they click Yes or No for splitting
    while True:
        splitclick = win.getMouse()
        splitclickX = splitclick.getX()
        splitclickY = splitclick.getY()
        hand1value = playervalue - playercard2
        hand2value = playervalue - playercard1

        #clicks on yes
        if splitclickX >= 1000 and splitclickX <= 1125 and splitclickY >= 190 and splitclickY <= 240:

            splitchoice = "yes"
            #increases the pot size (doubles the bet)
            pot.setText("${0}".format(int(bet)*2))

            #creates the box that keeps track of the value of the second hand
            splitplayerscore = Rectangle(Point(1083,385),Point(1138,415))
            splitplayerscore.setFill('white')
            splitplayerscore.draw(win)

            playerscore2 = Text(Point(1110.5,400),"")
            playerscore2.draw(win)

            if playervalue == 12:
                playerscore.setText(11)
                playerscore2.setText(11)

            else:
                playerscore.setText(hand1value)
                playerscore2.setText(hand2value)

            #moves the second card to the new location
            secondplayer.move(800,0)

            money = money - int(bet)
            balance.setText("${0}".format(money))
            splittext.undraw()
            yessplit.undraw()
            nosplit.undraw()
            yestext.undraw()
            notext.undraw()

            sleep(0.5)

            #calls the Double Down function and adjusts the pot size and balance accordingly
            DDhand1,DDhand2 = DoubleDown(win,splitchoice)
            if DDhand1 == "yes" and DDhand2 == "yes":
                pot.setText("${0}".format(int(bet)*4))
                money = money - 2* int(bet)
                balance.setText("${0}".format(money))
            elif DDhand1 == "yes" and DDhand2 == "no":
                pot.setText("${0}".format(int(bet)*3))
                money = money - int(bet)
                balance.setText("${0}".format(money))
            elif DDhand1 == "no" and DDhand2 == "yes":
                pot.setText("${0}".format(int(bet)*3))
                money = money - int(bet)
                balance.setText("${0}".format(money))
            elif DDhand1 == "no" and DDhand2 == "no":
                nothing = 1


            #creates the text on the window that lets the user know which hand they are on
            handcountertext = Text(Point(862.5,250),"Hand 1's Turn")
            handcountertext.setSize(28)
            handcountertext.setTextColor('white')
            handcountertext.draw(win)


            #infinite loop that gets the users click to see if they hit or stand on the current hand
            while True:
                #Allows the user to hit on the first hand until it's value is 21 or higher (breaks out of loop if the value is > 21 or they stand)
                if splithandcounter == 1 and hand1value <= 21:
                    if hand1value == 21:
                        handcountertext.undraw()
                        splithandcounter = splithandcounter + 1
                        pass
                    else:
                        splitclick1 = win.getMouse()
                        splitclick1X = splitclick1.getX()
                        splitclick1Y = splitclick1.getY()

                #Allows the user hit on the second hand unless it's value is 21 or higher (breaks out of loop if the value is > 21 or they stand)
                elif splithandcounter == 2 and hand2value <=21:

                    if hand2value == 21:
                        hand2turn = Text(Point(862.5,250),"Hand 2's Turn")
                        hand2turn.setSize(28)
                        hand2turn.setTextColor('white')
                        hand2turn.draw(win)
                        sleep(1)
                        hand2turn.undraw()
                        splithandcounter = splithandcounter + 1
                        pass
                    else:
                        splitclick1 = win.getMouse()
                        splitclick1X = splitclick1.getX()
                        splitclick1Y = splitclick1.getY()
                else:
                    if splithandcounter == 1:
                        handcountertext.undraw()
                        hand1bust = Text(Point(862.5,250),"Hand 1 Bust")
                        hand1bust.setSize(28)
                        hand1bust.setTextColor('white')
                        hand1bust.draw(win)
                        sleep(1)
                        hand1bust.undraw()
                        splithandcounter = splithandcounter + 1
                        pass
                    elif splithandcounter == 2:
                        handcountertext.undraw()
                        hand2bust = Text(Point(862.5,250),"Hand 2 Bust")
                        hand2bust.setSize(28)
                        hand2bust.setTextColor('white')
                        hand2bust.draw(win)
                        sleep(1)
                        hand2bust.undraw()
                        splithandcounter = splithandcounter + 1
                        pass


                #clicks on hit
                if splitclick1X >= 100 and splitclick1X <= 200 and splitclick1Y >= 220 and splitclick1Y <= 280:
                    #if the user is on hand 1 they can hit until they get 21 or higher then move onto the next hand (unless they double downed, then they only get 1 extra card)
                    if splithandcounter == 1:
                        #calls the hit function
                        hand1value,nextcard,used = Hit(win,hand1value,cards,suits,hand1cardcounter,used,splithandcounter)
                        hand1cardcounter = hand1cardcounter + 1
                        hand1value = hand1value + nextcard
                        playerscore.setText(hand1value)
                        #checks if the user double downed on hand 1 - only allows them 1 extra card then moves onto the next hand
                        if DDhand1 == "yes":
                            splithandcounter = splithandcounter + 1
                            sleep(0.5)
                            handcountertext.undraw()
                            hand2turn = Text(Point(862.5,250),"Hand 2's Turn")
                            hand2turn.setSize(28)
                            hand2turn.setTextColor('white')
                            hand2turn.draw(win)
                        else:
                            pass

                    elif splithandcounter == 2:
                        #if the user is on hand 2 they can hit until they get 21 or higher then move onto the next hand which ends the function
                        if hand2value <= 21:
                            hand2value,nextcard,used = Hit(win,hand2value,cards,suits,hand2cardcounter,used,splithandcounter)
                            hand2cardcounter = hand2cardcounter + 1
                            hand2value = hand2value + nextcard
                            playerscore2.setText(hand2value)
                            if DDhand2 == "yes":
                                sleep(0.5)
                                hand2turn.undraw()
                                splithandcounter = splithandcounter + 1

                            else:
                                pass
                        else:
                            break


                    else:
                        break


                #clicks on stand
                elif splitclick1X >= 225 and splitclick1X <= 325 and splitclick1Y >= 220 and splitclick1Y <= 280:
                    #if the user is on hand 1 and clicks stand, they will move onto the next hand
                    if splithandcounter == 1:
                        handcountertext.undraw()
                        hand2turn = Text(Point(862.5,250),"Hand 2's Turn")
                        hand2turn.setSize(28)
                        hand2turn.setTextColor('white')
                        hand2turn.draw(win)
                        splithandcounter = splithandcounter + 1


                    #if the user clicks stand while on hand 2, it will break out of the loop and end the splitting function
                    elif splithandcounter == 2:
                        hand2turn.undraw()
                        break


            break

        #clicks on no for splitting
        elif splitclickX >= 1000 and splitclickX <= 1125 and splitclickY >= 260 and splitclickY <= 310:
            splitchoice = "no"
            DDhand1 = "no"
            DDhand2 = "no"
            splittext.undraw()
            yessplit.undraw()
            nosplit.undraw()
            yestext.undraw()
            notext.undraw()
            break

        #clicks outside of a box
        else:
            pass

    return splitchoice,hand1value,hand2value,DDhand1,DDhand2,money

#asks the user if they want insurance if the dealers face up card is an ace
def insurance(win,bet,money,balance):

    insurancetext = Text(Point(850,250),"Insurance?")
    insurancetext.setTextColor('white')
    insurancetext.setSize(20)
    insurancetext.draw(win)

    yesinsurance = Rectangle(Point(1000,190),Point(1125,240))
    yesinsurance.setFill("limegreen")
    yesinsurance.draw(win)

    noinsurance = Rectangle(Point(1000,260),Point(1125,310))
    noinsurance.setFill('firebrick')
    noinsurance.draw(win)

    yestext = Text(Point(1062.5,215),"YES")
    yestext.setSize(16)
    yestext.draw(win)

    notext = Text(Point(1062.5,285),"NO")
    notext.setSize(16)
    notext.draw(win)

    insurance = int(int(bet) / 2)

    #gets the user to click yes or no for insurance
    while True:
        insuranceclick = win.getMouse()
        insuranceclickX = insuranceclick.getX()
        insuranceclickY = insuranceclick.getY()

        if insuranceclickX >= 1000 and insuranceclickX <= 1125 and insuranceclickY >= 190 and insuranceclickY <= 240:
            insuranceanswer = "yes"
            money = money - (insurance)
            balance.setText("${0}".format(money))
            insurancetext.undraw()
            yesinsurance.undraw()
            noinsurance.undraw()
            yestext.undraw()
            notext.undraw()
            break


        elif insuranceclickX >= 1000 and insuranceclickX <= 1125 and insuranceclickY >= 260 and insuranceclickY <= 310:
            insuranceanswer = "no"
            insurancetext.undraw()
            yesinsurance.undraw()
            noinsurance.undraw()
            yestext.undraw()
            notext.undraw()
            break

        else:
            pass
    return money,balance,insuranceanswer,insurance


#allows the user to make a bet before the game begins
def makeABet(win,betbox,balance,startbutton,money):

    #breaks out of the loop and the game starts when they user submits their bet
    while True:
        betclick = win.getMouse()
        betX = betclick.getX()
        betY = betclick.getY()

        if betX >= 600 and betX <= 700 and betY >= 550 and betY <= 600:
            bet = betbox.getText()
            if bet.isdigit() and int(bet) <= money and int(bet) >= 50:
                betbox.setText("")
                startbutton.setFill('grey')
                money = money - int(bet)
                balance.setText("${0}".format(money))
                pot = Text(Point(1012.5,575),"${0}".format(bet))
                pot.setSize(18)
                pot.setTextColor('white')
                pot.draw(win)
                break

                betbox.setText("")
            else:
                pass


    return bet,money,pot


#creates the function that is used at the end of the game where the player will decide to quit the game or play again
def playagain(win):
    #creates the play again button
    continuebutton = Rectangle(Point(1000,190),Point(1125,240))
    continuebutton.setFill("limegreen")
    continuebutton.draw(win)
    #creates the quit button
    quitbutton = Rectangle(Point(1000,260),Point(1125,310))
    quitbutton.setFill('firebrick')
    quitbutton.draw(win)

    continuetext = Text(Point(1062.5,215),"Continue")
    continuetext.setSize(14)
    continuetext.draw(win)

    quittext = Text(Point(1062.5,285),"Quit")
    quittext.setSize(14)
    quittext.draw(win)

#Compares the final values of the dealer and the player and determines who the winner is
def compare(win,finalplayervalue,finaldealervalue,playercard1,playercard2,balance,bet,money,doubledownhand1):
    #if the players score is higher than the dealers score without busting, or if the dealer busts, the player wins
    if (finalplayervalue > finaldealervalue and finalplayervalue <= 21) or (finalplayervalue <= 21 and finaldealervalue > 21):
        if playercard1 + playercard2 == 21:
            pass
        elif finaldealervalue > 21:
            busttext = Text(Point(862.5,250),"Dealer Bust")
            busttext.setSize(28)
            busttext.setTextColor('white')
            busttext.draw(win)
            sleep(1)
            busttext.undraw()
            winner = Text(Point(862.5,250),"You Win")
            winner.setSize(28)
            winner.setTextColor('white')
            winner.draw(win)
            if doubledownhand1 == "no":
                money = money + (2*(int(bet)))
                balance.setText("${0}".format(money))
            else:
                money = money + (4*(int(bet)))
                balance.setText("${0}".format(money))
        else:
            winner = Text(Point(862.5,250),"You Win")
            winner.setSize(28)
            winner.setTextColor('white')
            winner.draw(win)
            if doubledownhand1 == "no":
                money = money + (2*(int(bet)))
                balance.setText("${0}".format(money))
            else:
                money = money + (4*(int(bet)))
                balance.setText("${0}".format(money))
    #if the dealers score is higher than the players score without busting, or if the player busts, the dealer wins
    elif (finaldealervalue > finalplayervalue and finaldealervalue <= 21) or (finaldealervalue <= 21 and finalplayervalue > 21):
        winner = Text(Point(862.5,250),"Dealer Wins")
        winner.setSize(28)
        winner.setTextColor('white')
        winner.draw(win)

    #if both scores are the same, it is a push (unless they are both blackjack - the player wins)
    elif finalplayervalue == finaldealervalue:
        money = money + int(bet)
        push = Text(Point(862.5,250),"Push")
        push.setSize(28)
        push.setTextColor('white')
        push.draw(win)
        if doubledownhand1 == "no":
            money = money
            balance.setText("${0}".format(money))
        else:
            money = money + ((int(bet)))
            balance.setText("${0}".format(money))
    return money

#checks if the player gets a blackjack in the first two cards dealt to them
def checkWinnerFirstTwoCards(dealervalue,playervalue,win,graphdealer1,dealervaluegraph,money,bet,dealercard2):
    #if the player gets 21 on the first two cards, they win
    if (playervalue == 21 and dealervalue <= 21):
        winner = "Player"
        blackjack = Text(Point(862.5,250),"Blackjack")
        blackjack.setSize(28)
        blackjack.setTextColor('white')
        blackjack.draw(win)
        sleep(1.5)
        blackjack.undraw()
        dealerflip = Image(Point(125,100),graphdealer1 + ".gif")
        dealerflip.draw(win)
        youwin = Text(Point(862.5,250),"You Win")
        youwin.setSize(28)
        youwin.setTextColor('white')
        youwin.draw(win)
        dealervaluegraph.setText(dealervalue)
        money = money + (3*int(bet))

    elif dealervalue == 21 and playervalue < 21 and dealercard2 == 11:
        winner = "Dealer"
    else:
        winner = "None"
    return winner,money

#deals the first two cards to the dealer and the player, and returns the current scores
def FirstTwoCards(used):
    #creates the cards and suits list
    cards = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    suits = ["d","h","s","c"]

    #infinite loop that keeps dealing cards until all 4 of the first cards are different (to simulate a single deck)
    while True:
        #randomly selects the cards
        card1 = cards[randint(0,12)]
        card2 = cards[randint(0,12)]

        if card1 == card2:
            splittingoption = "yes"
        else:
            splittingoption = "no"

        #creates the "graph" value of the cards (ex: c8 = 8 of clubs) that will be used to display the picture of the card in the window
        if card1.isalpha() or card2.isalpha():
            if card1.isalpha() and card2.isalpha():
                graphcard1 = suits[randint(0,3)] + card1.lower()
                #adds the cards to the "used" list to prevent them from being dealt again in the future
                used.append(graphcard1)
                graphcard2 = suits[randint(0,3)] + card2.lower()
                used.append(graphcard2)
            if card1.isalpha():
                graphcard1 = suits[randint(0,3)] + card1.lower()
                used.append(graphcard1)
                graphcard2 = suits[randint(0,3)] + card2
                used.append(graphcard2)
            if card2.isalpha():
                graphcard2 = suits[randint(0,3)] + card2.lower()
                used.append(graphcard2)
                graphcard1 = suits[randint(0,3)] + card1
                used.append(graphcard1)

        else:
            graphcard1 = suits[randint(0,3)] + card1
            used.append(graphcard1)
            graphcard2 = suits[randint(0,3)] + card2
            used.append(graphcard2)

        #makes sure the cards are used twice maximum (2 deck)
        if used.count(graphcard1) <= 2 and used.count(graphcard2) <= 2:
            #changes the card value into an integer to be added for the current score
            if card1 == "2" or card1 == "3" or card1 == "4" or card1 == "5" or card1 == "6" or card1 == "7" or card1 == "8" or card1 == "9" or card1 == "10":
                card1 = int(card1)
            if card2 == "2" or card2 == "3" or card2 == "4" or card2 == "5" or card2 == "6" or card2 == "7" or card2 == "8" or card2 == "9" or card2 == "10":
                card2 = int(card2)
            #makes the value 10 if the card is a jack, queen or king
            if card1 == "J" or card1 == "Q" or card1 == "K":
                card1 = 10
            if card2 == "J" or card2 == "Q" or card2 == "K":
                card2 = 10
            #makes aces worth either 1 or 11 (will be a 1 if the 11 will make you bust)
            if card1 == "A" or card2 == "A":
                if card1 == "A" and card2 == "A":
                    card1 = 1
                    card2 = 11
                    #creates the "graph" value for the aces
                    graphcard1 = suits[randint(0,3)]+"1"
                    graphcard2 = suits[randint(0,3)]+"1"

                elif card1 == "A":
                    graphcard1 = suits[randint(0,3)]+"1"
                    if card2 <=10:
                        card1 = 11
                else:
                    graphcard2 = suits[randint(0,3)]+"1"
                    if card1 <= 10 and card2 == "A":
                        card2 = 11


            value = card1 + card2
            break
        else:
            pass
    return card1,card2,value,graphcard1,graphcard2,used,splittingoption


#displays the first two cards for the dealer and the player in the window in their designated spots
def graphFirstTwo(win,graphdealer1,graphdealer2,graphplayer1,graphplayer2):
    #the dealers first card will be flipped upside down until the player ends their turn
    sleep(0.5)
    firstdealer = Image(Point(125,100),"b1fv.gif")
    firstdealer.draw(win)
    sleep(0.5)
    firstplayer = Image(Point(125,400),graphplayer1 + ".gif")
    firstplayer.draw(win)
    sleep(0.5)
    seconddealer = Image(Point(225,100),graphdealer2 + ".gif")
    seconddealer.draw(win)
    sleep(0.5)
    secondplayer = Image(Point(225,400),graphplayer2 + ".gif")
    secondplayer.draw(win)

    return secondplayer


#gets the player to decide hit or stand
def Player(win,playervalue,dealervalue,playervaluegraph,playercard1,playercard2,used,playersplit,splithandcounter,doubledownhand1):


    cards = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    suits = ["d","h","s","c"]
    #initiates the card counter as 2 (since the player already has 2 cards)
    cardcounter = 2
    #initiates the ace count
    acecount = 0
    #initiates the minus count (makes sure 10 is only subtracted from the score once) for when you have an ace worth 11 that will make you bust
    minuscount = 0

    #creates an infinite loop that breaks when the player clicks stand, busts, or gets blackjack
    while True:
        if playervalue >= 21:
            if playervalue > 21:
                busttext = Text(Point(862.5,250),"You Bust")
                busttext.setSize(28)
                busttext.setTextColor('white')
                busttext.draw(win)
                sleep(1)
                busttext.undraw()
                break
            elif playervalue == 21:
                twentyone = Text(Point(862.5,250),"Twenty One")
                twentyone.setSize(28)
                twentyone.setTextColor('white')
                twentyone.draw(win)
                sleep(1)
                twentyone.undraw()
                break

        click = win.getMouse()
        clickX = click.getX()
        clickY = click.getY()

        #player clicks hit
        if clickX >= 100 and clickX <= 200 and clickY >= 220 and clickY <= 280:
            #calls the hit function
            playervalue,nextcard,used = Hit(win, playervalue,cards,suits,cardcounter,used,splithandcounter)
            #adds the new card to the current score
            playervalue = playervalue + nextcard
            #adds one to the card counter
            cardcounter = cardcounter + 1
            #if the next card is an ace, then 1 will be added to the ace count
            if nextcard == 11 or playercard1 == 11 or playercard2 == 11:
                acecount = acecount + 1
            #if the minus count is 0 and the next card will make you bust and you have an ace, 10 will be subtracted from your score
            if minuscount == 0:
                if playervalue > 21 and acecount > 0:
                    playervaluegraph.setText(playervalue)
                    playervalue = playervalue - 10
                    #adds 1 to the minus count so the subtraction only happens once
                    minuscount = minuscount + 1
            #updates the score box on the left side of the window
            playervaluegraph.setText(playervalue)

            #makes it so you only get one extra card if you double down
            if doubledownhand1 == "yes":
                dealersturn = Text(Point(862.5,250),"Dealers Turn")
                dealersturn.setSize(28)
                dealersturn.setTextColor('white')
                dealersturn.draw(win)
                sleep(1)
                dealersturn.undraw()
                break

        #player clicks stand - breaks out of the loop and moves on to the dealer function (called from main())
        elif clickX >= 225 and clickX <= 325 and clickY >= 220 and clickY <= 280:
            dealersturn = Text(Point(862.5,250),"Dealers Turn")
            dealersturn.setSize(28)
            dealersturn.setTextColor('white')
            dealersturn.draw(win)
            sleep(1)
            dealersturn.undraw()
            break
        #nothing happens if the player doesn't click hit or stand
        else:
            pass

    return cards,suits,playervalue


#a new card will be dealt to the player in this function if they click hit
def Hit(win,playervalue,cards,suits,cardcounter,used,splithandcounter):

    #creates an infinite loop that deals a card to the player until the card has not been dealt to the player or dealer before more than twice
    while True:

        nextcard = cards[randint(0,12)]

        #creates the "graph" value of the card
        if nextcard.isalpha():
            if nextcard == "A":
                graphcard = suits[randint(0,3)] + "1"
            else:
                graphcard = suits[randint(0,3)] + nextcard.lower()
        else:
            graphcard = suits[randint(0,3)] + nextcard

        #makes sure the card has not been used before or only been used once
        if used.count(graphcard) <= 1:
            #assigns the card its numeric value
            if nextcard == "J" or nextcard == "Q" or nextcard =="K":
                nextcard = 10
            elif nextcard == "A":
                if playervalue <= 10:
                    nextcard = 11
                else:
                    nextcard = 1
            else:
                nextcard = int(nextcard)
            #adds the card to the used list
            used.append(graphcard)
            #displays the card in the window in it's right place (using cardcounter to find the x coordinate)
            if splithandcounter == 1:
                xvalue = cardcounter * 100
            elif splithandcounter == 2:
                xvalue = 900 - (cardcounter * 100)
            else:
                xvalue = cardcounter * 100
            Image(Point(125 + xvalue,400),graphcard+".gif").draw(win)
            return playervalue,nextcard,used
            break

#deals cards to the dealer until their score is 17 or higher
def Dealer(win,dealervalue,dealervaluegraph,dealercard1,dealercard2,finalplayervalue,used,graphdealer1,splitchoice):
     cards = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
     suits = ["d","h","s","c"]
    #initiates the card counter as 2
     cardcounter = 2
     #initiates the acecount as 0
     acecount = 0
     #initiates the minus count as 0
     minuscount = 0
     #flips the dealers first card up right so the player can see what it was
     dealerflip = Image(Point(125,100),graphdealer1 + ".gif")
     dealerflip.draw(win)
     #adds the flipped over cards value to the score box on the left of the window
     dealervaluegraph.setText(dealervalue)
     sleep(0.75)

     #infinite loop that deals cards until the dealers value is 17 or higher
     while True:
        #skips the dealers turn if the player busted which means the dealer won
        if finalplayervalue > 21 and splitchoice == "no":
            break
        #draws cards until the dealers value is 17 or higher
        else:
            if dealervalue < 17:
                #infinite loop that deals cards until the card has not been dealt to the player or dealer yet more than twice
                while True:
                    nextcard = cards[randint(0,12)]
                    #creates the "graph" value of the card
                    if nextcard.isalpha():
                        if nextcard == "A":
                            graphcard = suits[randint(0,3)] + "1"
                        else:
                            graphcard = suits[randint(0,3)] + nextcard.lower()
                        #assigns the card to its numeric value
                        if nextcard == "J" or nextcard == "Q" or nextcard =="K":
                            nextcard = 10
                        elif nextcard == "A":
                            if dealervalue <= 10:
                                nextcard = 11
                            else:
                                nextcard = 1
                    else:
                        graphcard = suits[randint(0,3)] + nextcard
                        nextcard = int(nextcard)

                    #makes sure the card hasn't been used yet or has only been used once
                    if used.count(graphcard) <= 1:
                        #updates the dealers score
                        dealervalue = dealervalue + nextcard

                        if nextcard == 11 or dealercard1 == 11 or dealercard2 == 11:
                                acecount = acecount + 1

                        if minuscount == 0:
                            if dealervalue > 21 and acecount > 0:
                                dealervalue = dealervalue - 10
                                minuscount = minuscount + 1
                        #adds the card to the used list
                        used.append(graphcard)
                        #displays the card in the window
                        xvalue = cardcounter * 100
                        Image(Point(125 + xvalue,100),graphcard+".gif").draw(win)
                        cardcounter = cardcounter + 1
                        #updates the score box on the left of the window
                        dealervaluegraph.setText(dealervalue)
                        sleep(0.75)
                        break

            else:
                break

     return dealervalue,used

#makes the Blackjack board layout
def MakeLayout():
    #creates the window and background
    win = GraphWin("Black Jack",1150, 650)
    win.setBackground("darkgreen")

    #makes the line that separates the betting options
    separate = Line(Point(0,500),Point(1150,500))
    separate.setFill("white")
    separate.setWidth(4)
    separate.draw(win)

    #creates the dealer and player score boxes at the left of the window
    dealerscore = Rectangle(Point(12,85),Point(67,115))
    dealerscore.setFill('white')
    dealerscore.draw(win)

    playerscore = Rectangle(Point(12,385),Point(67,415))
    playerscore.setFill('white')
    playerscore.draw(win)

    #creates the HIT and STAND buttons
    hit = Rectangle(Point(100,220),Point(200,280))
    hit.setFill('limegreen')
    hit.draw(win)
    hittext = Text(Point(150,250),"HIT")
    hittext.setSize(16)
    hittext.draw(win)

    stand = Rectangle(Point(225,220),Point(325,280))
    stand.setFill('firebrick')
    stand.draw(win)
    standtext = Text(Point(275,250),"STAND")
    standtext.setSize(16)
    standtext.draw(win)

    #Creates the player's card slots (white rectangles around the cards)
    rectangle1 = Rectangle(Point(80,340),Point(170,460))
    rectangle1.setOutline('white')
    rectangle1.draw(win)
    rectangle2 = Rectangle(Point(180,340),Point(270,460))
    rectangle2.setOutline('white')
    rectangle2.draw(win)
    rectangle3 = Rectangle(Point(280,340),Point(370,460))
    rectangle3.setOutline('white')
    rectangle3.draw(win)
    rectangle4 = Rectangle(Point(380,340),Point(470,460))
    rectangle4.setOutline('white')
    rectangle4.draw(win)
    rectangle5 = Rectangle(Point(480,340),Point(570,460))
    rectangle5.setOutline('white')
    rectangle5.draw(win)
    rectangle6 = Rectangle(Point(580,340),Point(670,460))
    rectangle6.setOutline('white')
    rectangle6.draw(win)
    rectangle7 = Rectangle(Point(680,340),Point(770,460))
    rectangle7.setOutline('white')
    rectangle7.draw(win)
    rectangle8 = Rectangle(Point(780,340),Point(870,460))
    rectangle8.setOutline('white')
    rectangle8.draw(win)
    rectangle9 = Rectangle(Point(880,340),Point(970,460))
    rectangle9.setOutline('white')
    rectangle9.draw(win)
    rectangle10 = Rectangle(Point(980,340),Point(1070,460))
    rectangle10.setOutline('white')
    rectangle10.draw(win)

    #creates the dealers card slots (white rectangles around the cards)
    rectangle11 = Rectangle(Point(80,160),Point(170,40))
    rectangle11.setOutline('white')
    rectangle11.draw(win)
    rectangle12 = Rectangle(Point(180,160),Point(270,40))
    rectangle12.setOutline('white')
    rectangle12.draw(win)
    rectangle13 = Rectangle(Point(280,160),Point(370,40))
    rectangle13.setOutline('white')
    rectangle13.draw(win)
    rectangle14 = Rectangle(Point(380,160),Point(470,40))
    rectangle14.setOutline('white')
    rectangle14.draw(win)
    rectangle15 = Rectangle(Point(480,160),Point(570,40))
    rectangle15.setOutline('white')
    rectangle15.draw(win)
    rectangle16 = Rectangle(Point(580,160),Point(670,40))
    rectangle16.setOutline('white')
    rectangle16.draw(win)
    rectangle17 = Rectangle(Point(680,160),Point(770,40))
    rectangle17.setOutline('white')
    rectangle17.draw(win)
    rectangle18 = Rectangle(Point(780,160),Point(870,40))
    rectangle18.setOutline('white')
    rectangle18.draw(win)
    rectangle19 = Rectangle(Point(880,160),Point(970,40))
    rectangle19.setOutline('white')
    rectangle19.draw(win)
    rectangle20 = Rectangle(Point(980,160),Point(1070,40))
    rectangle20.setOutline('white')
    rectangle20.draw(win)

    #Text in the middle of the board
    blackjack = Text(Point(575,250),"Blackjack")
    blackjack.setSize(36)
    blackjack.setStyle('bold italic')
    blackjack.draw(win)

    #Text that shows the dealers side of the board
    dealertext = Text(Point(575,180),"Dealer")
    dealertext.setSize(16)
    dealertext.draw(win)

    #Text that shows the players side of the board
    playertext = Text(Point(575,320),"Player")
    playertext.setSize(16)
    playertext.draw(win)

    return win,rectangle2,rectangle9

#creats the layout for the betting portion of the game (under the cards)
def BetLayout(win,money):

    balance = Text(Point(137.5,575),"${0}".format(money))
    balance.setSize(18)
    balance.setTextColor('white')
    balance.draw(win)

    betquestion = Text(Point(575,525),"Enter your bet (minimum $50)")
    betquestion.setTextColor('white')
    betquestion.setSize(18)
    betquestion.draw(win)

    betquestionunderline = Line(Point(420,540),Point(730,540))
    betquestionunderline.setFill('white')
    betquestionunderline.setWidth(2)
    betquestionunderline.draw(win)

    moneysymbol = Text(Point(475,575),"$")
    moneysymbol.setTextColor('white')
    moneysymbol.setSize(20)
    moneysymbol.draw(win)


    betbox = Entry(Point(525,575),7)
    betbox.draw(win)

    startbutton = Rectangle(Point(600,550),Point(700,600))
    startbutton.setFill("green")
    startbutton.draw(win)


    starttext = Text(Point(650,575),"START")
    starttext.setSize(18)
    starttext.draw(win)

    divideline = Line(Point(275,500),Point(275,650))
    divideline.setWidth(4)
    divideline.setFill('white')
    divideline.draw(win)

    divideline2 = Line(Point(875,500),Point(875,650))
    divideline2.setWidth(4)
    divideline2.setFill('white')
    divideline2.draw(win)

    banktitle = Text(Point(137.5,525),"Balance")
    banktitle.setTextColor('white')
    banktitle.setSize(18)
    banktitle.draw(win)

    pottitle = Text(Point(1012.5,525),"Bet")
    pottitle.setTextColor('white')
    pottitle.setSize(18)
    pottitle.draw(win)

    pottitleunderline = Line(Point(995,540),Point(1035,540))
    pottitleunderline.setFill('white')
    pottitleunderline.setWidth(2)
    pottitleunderline.draw(win)

    banktitleunderline = Line(Point(90.5,540),Point(185.5,540))
    banktitleunderline.setFill('white')
    banktitleunderline.setWidth(2)
    banktitleunderline.draw(win)

    return betbox,balance,startbutton


#calls the main function
main()
