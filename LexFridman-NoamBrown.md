# Noam Brown: AI vs Humans in Poker and Games of Strategic Negotiation | Lex Fridman Podcast #344

**Video:** [https://www.youtube.com/watch?v=2oHH4aClJQs](https://www.youtube.com/watch?v=2oHH4aClJQs)
**Channel:** Lex Fridman
**Duration:** 2:29:21
**Upload date:** 2022-12-06
**Source:** Auto-generated English captions (YouTube)

---

**[00:00]** a lot of people were saying like oh this whole idea of Game Theory it's just nonsense and if you really want to make money you got to like look into the other person's eyes and read their soul and figure out what cards they have but what happened was where we played our bot against four top heads up no limit Hold'em poker players and the bot wasn't trying to adapt to them it wasn't trying to exploit them it wasn't trying to do

**[00:20]** these Mind Games it was just trying to approximate the Nash equilibrium and it crushed them

**[00:28]** the following is a conversation with no Brown research scientists at Fair Facebook AI research group at meta AI he co-created the first AI system that achieved superhuman level performance in No Limit Texas Hold'em both heads up and multiplayer and now recently he

**[00:46]** co-created an AI system that can strategically out-negotiate humans using natural language in a popular board game called diplomacy which is a war game that emphasizes negotiation

**[00:59]** this is a Lex Friedman podcast to support it please check out our sponsors in the description and now dear friends here's gnome proud

**[01:09]** you've been a lead on three amazing AI projects so we've got libratus that solved or at least achieved human level performance on No Limit Texas Hold'em poker with two players heads up you got pluribus that solved No Limit Texas HoldEm Poker with six players and just now you have Cicero these are all names of systems that solved or achieved human level performance on the game of diplomacy which for people who don't know is a popular strategy board game it

**[01:39]** was loved by JFK John F Kennedy and Henry Kissinger and many other big

**[01:49]** famous people in the decades since so let's talk about poker and diplomacy today first poker what is the game of No Limit Texas Hold'em and how's it different from chess well no limit Texas hold 'em poker is the most popular variant of Poker in the world so you know you go to a casino you play sit down at the poker table the game that you're playing is no limit Texas Hold'em if you watch movies about poker like Casino Royale or rounders the game that

**[02:12]** they're playing is no limit Texas hold in poker now it's very different from limit Hold'em in that you can bet any amount of chips that you want and so the stakes escalate really quickly you start out with like one or two dollars in the pot and then by the end of the hand you've got like a thousand dollars in there maybe so the option to increase the number of very aggressively very quickly is always there right the No Limit

**[02:35]** aspect is there's no limit to how much you can bet you know you in limit Hold'em there's like two dollars in the Pod you you can only bet like two dollars but if you got ten thousand dollars in front of you you're always welcome to put ten thousand dollars into the pot so I've got a chance to hang out with uh Phil Hellmuth who plays all these different variants of Poker and correct me if I'm wrong but it seems like no limit rewards crazy versus the

**[02:58]** other ones rewards more kind of calculated strategy or or no because you're sort of looking from an from an analytic perspective is is strategy also

**[03:12]** rewarded in No Limit taxes hold on I think both variance reward strategy but I think what's different about No Limit Hold'em is it's it's much easier to get jumpy you know you go in there thinking you're going to lose you're going to play for like a hundred dollars or something and suddenly there's like you know a thousand dollars in the pot a lot of people can't handle that can you define jumpy when you're playing poker

**[03:32]** you always want to choose the action that's going to maximize your expected value it's kind of like kind of like with investing right like if you're ever in a situation where you're the amount of money that's at stake is um is going to have a material impact on your life then you're going to play in a more risk-averse style you know if somebody makes a huge bet you're gonna if you're playing no limit hold them and somebody makes a huge bet

**[03:55]** there might come a point where you're like this is too much money for me to handle like I can't risk this amount uh and that's what throws a lot of people off so that's the big difference I think between No Limit and limit what about on the action side when you're actually making that big bet that's what I mean by crazy I was I was trying to refer to the technical the the technical term of crazy meaning use the big jump in the

**[04:20]** BET to completely throw off the other person in terms of um their ability to reason optimally I think that's right I think one of the key strategies in poker is to put the other person into an uncomfortable position and if you're doing that then you're you're playing poker well and there's a lot of opportunities to do that in no limit Hold'em you know you can have like 50 in there you throw in a thousand dollar bet and um you know that's sometimes if you

**[04:47]** do it right it puts the other person in a really tough spot now it's also possible that you make huge mistakes that way and so it's really easy to lose a lot of money and no limit hold them if you don't know what you're doing um but there's a lot of upside potential too so when you build systems AI systems that play these games we'll talk about poker we'll talk about diplomacy are you um are you drawn in in part by the beauty of the game itself AI aside

**[05:11]** or is it to you primarily a fascinating

**[05:17]** problem set for the eye to solve I'm drawn in by the beauty of the game uh when I I started playing poker when I was in high school and the idea to me that there is a correct and objectively correct way of playing poker and if you could figure out what that is then you're you know you're making unlimited money basically that's like a really fascinating concept to me um and so I was fascinated by the strategy of Poker even when I was like

**[05:42]** 16 years old it wasn't until like much later that I actually worked on poker AIS so there was a sense that you can solve poker like uh in the way you can solve chess for example or Checkers I believe Checkers got solved right yeah Checkers Checkers are completely solved up optimal optimal strategy it's impossible to beat the AI yeah and so in that same way you could technically solve chess you could solve chess you could solve

**[06:05]** poker you could solve poker so this is this gets into the concept of an ash equilibrium yeah so it is a Nash equilibrium Okay so

**[06:16]** and any finite two-player zero-sum game there is an optimal strategy that if you play it you are guaranteed to not lose an expectation no matter what your opponent does and this is kind of a radical concept to a lot of people um but it's true in chess it's true in poker it's true in any finite two-player zero-sum game and to give some intuition for this you can think of rock paper scissors and rock paper scissors if you randomly

**[06:38]** choose between throwing rock paper and scissors with equal probability then no matter what your opponent does you are not going to lose an expectation you're not going to lose an expectation in the long run now the same is true for poker there exists some strategy some really complicated strategy that if you play that you are guaranteed to not lose money in the long run and I should say this is for two player poker six player

**[07:00]** poker is a different story yeah it's a beautiful giant mess when you say in expectation you're guaranteed not to lose in expectation what does in expectation mean Poker is a very high variance game so you're gonna have hands where you win you're gonna have hands with your lose even if you're playing the perfect strategy you can't guarantee they're going to win every single hand but if you play for long enough then you

**[07:20]** are guaranteed to at least break even and and practice probably one so that's an expectation the size of your stack generally speaking now that doesn't include anything about the fact that you can go broke it doesn't include any of those kinds of normal real world limitations you're talking you know in the theoretical world uh what about this the zero-sum aspect how big of a constraint is that how big of a constraint is finite

**[07:46]** so finite's not a huge constraint so I mean most games that you play are finite in size um it's also true actually that there exists this like perfect strategy in many infinite games as well technically the game has to be compact um there are like some edge cases where you don't have an ash equilibrium and a two player zero-sum game so you can think of a game where you like you know if we're playing a game where whoever

**[08:08]** names the bigger number is the winner there's no Nash equilibrium to that game 17 yeah 18. but you beat you win again you're good at this I played a lot of games okay uh so that's and then the Zero Sum aspect the zero zero sum aspects so there exists a Nash equilibrium in non two player zero-sum games as well and by the way just to clarify what I mean by two player Zero Sum I mean there's two players and whatever one player wins the

**[08:34]** other player loses so if we're applying poker and I win 50 that means that you're losing fifty dollars now outside of two player zero-sum games there still exists Nash equilibria but they're not as meaningful because you know you can think of a game like Risk if everybody else at the and on the board decides a team up against you and take you out there's no perfect strategy you can play that's gonna guarantee that you win there there's just nothing you

**[08:58]** can do so outside of two players zero some games there's no guarantee that you're going to win by playing a national equilibrium have you ever tried to model in the other aspects of the game which is like the pleasure you draw from playing the game and then if you're a professional poker player if you're exciting even if you lose uh the you know the money you would get from the attention you get to the sponsor and all that kind of stuff is

**[09:25]** that that would be a fun thing to model to model in as I'd be make it sort of super complex to include the human factor in this in this full complexity I think you bring up a couple good points there so I think a lot of professional poker players I mean they got a huge amount of money not from actually playing poker but from the sponsorships and having a personality that people want to tune in and watch that that's a big that's a big way to to make a name

**[09:50]** for yourself in poker I just wanted from an AI perspective if you create and we'll talk about this more maybe a AI system that also talks trash and all that kind of stuff that that becomes part of the function to maximize so it's not just optimal poker play maybe sometimes you want to be chaotic maybe sometimes you want to be suboptimal and you lose um the the chaos and maybe sometimes you want to be overly aggressive because

**[10:16]** people the audience loves that

**[10:21]** that's fascinating I think I think what you're getting at here is that there's a difference between making an AI that wins a game and an AI That's fun to play with right yeah yeah and more fun to watch so those are all different things fun to play with and fun to watch yeah and I think you know I've I've heard uh talks from like game designers and and they say like you know people that work on AI for actual recreational games that

**[10:39]** people play and they say yeah there's a big difference between trying to make an area that actually wins and you know you look at a game like Civilization um the way that the AIS play is not optimal for trying to win they're they're playing a different game they're trying to have personalities they're trying to be fun and engaging um and that makes for a better game yeah and we also talk about NPCs I just talked to Todd Howard who is the the

**[11:03]** creator of Fallout in the Elder Scrolls series and um Starfield the new game coming out and the Creator what I think is the greatest game of all time which is Skyrim and the NPCs there the AI that governs that whole game is very interesting but the NPCs also are super interesting and considering what language models might do to NPCs in an open world RPG

**[11:28]** role-playing game it's super exciting yeah honestly I'm I think this is like one of the first applications where we're going to see like real consumer interaction with large language models um I guess what sky um Elder Scrolls 6 is in development now they're probably like pretty close to finishing it but I would not be surprised at all if Elder Scrolls 7 was using large language models for their NPCs no they're not they're I mean I'm not saying anything

**[11:50]** not saying anything this is me speculating not you no but but there's they're just releasing the star feel good they do one game at a time yeah and so uh whatever it is whenever the date is I don't know what the data is calm down uh but it would be I don't know like uh 20 24 25 26 so it's actually very possible they would include language models I was listening to this um this talk by a gaming executive uh when I was in grad school

**[12:19]** and one of the questions that a person in the audience asked is why are all these games so focused on fighting and killing and the person responded that it's just so much harder to make an AI that can talk with you and cooperate with you than it is to make an AI that can fight you and I think once this technology develops further and you can have a you can reach a point where like not every single line of dialogue has to be

**[12:42]** scripted it unlocks a lot of potential for new kinds of games like much more like positive interactions that are not so focused on fighting and I'm really looking forward to that well it might not be positive it might be just drama you'll be in like a Call of Duty game instead of doing the shooting you'll just be hanging out and like arguing with an AI about like um like passive aggressive and then you won't be able to sleep that night you

**[13:04]** have to return or continue the argument that you were uh emotionally hurt uh

**[13:12]** I mean yeah I think that's actually an exciting World whatever whatever is the drama the chaos that we love the push and pull of human connection I think it's possible to do that in the video game world and I think you could be Messier and make more mistakes in the Video Game World which is why it would be a nice place and and also it doesn't have a deep of a as deep of a real psychological impact because inside video games it's kind of understood that

**[13:34]** you're in a not a real world so whatever crazy stuff AI does we have some flexibility to play just like with the game of diplomacy it's a game this is not real geopolitics not real war it's a it's a game so you could you can have a little bit of fun a little bit of chaos okay back to Natural uh how do we find the Nash equilibrium all right so there's different ways to find an ash equilibrium so um the way that we do it is with this

**[14:03]** process called self-play um basically we have this algorithm that starts by playing totally randomly and it learns how to play the game by playing against itself so um it will start playing the game totally randomly and then it you know if it's playing poker it'll eventually like get to the end of the end of the game and make fifty dollars and then it will like review all the decisions that it made along the way and say what would have happened if I had

**[14:30]** chosen this other action instead you know if I had raised here instead of called um what would the other player have done and because it's playing against a copy of itself it's able to do that counterfactual reasoning so they can say okay well if I took this action and the other person takes this action and then I take this action and eventually I make 150 instead of 50. and so it updates the regret value for that action

**[14:55]** regret is basically like how much does it regret having not played that action in the past and when it encounters that same situation again it's going to pick actions that have higher regret with higher probability now it'll just keep simulating the games this way it'll keep um you know accumulating regrets for different situations um and in the long run if you pick actions that have higher regret with higher probability in the correct way

**[15:18]** it's proven to converge to a Nash equilibrium even for super complex games even for imperfect information games it's true for all games it's true for it's true for chess it's true for poker it's particularly useful for poker so this is the the method of contractual regret minimization this is counter factual regret minimization that doesn't have to do with self-play has to do with just any any if you follow this kind of

**[15:40]** process self-play or not you'll be able to arrive in an optimal set of actions so this counterfactual regret minimization is a kind of self-play it's a principled kind of self-play that's proven to converge to Nash equilibria even in in private information games now you can have other forms of self-play and people use other forms of self-play for perfect information games um where you have more flexibility the algorithm doesn't have to be as

**[16:05]** theoretically sound in order to converge to that class of games because there's uh it's a simpler setting sure so I kind of in my brain the word self-play has mapped in you all networks but we're speaking something bigger than just neural networks it could be anything the self-play mechanism is just the mechanism of a system playing itself exactly yeah self-play is not tied specifically to neural Nets it's it's a kind of reinforcement learning basically

**[16:29]** okay and I would also say this process of like trying to reason oh what would the value have been if I had taken this other action instead this is very similar to how humans learn to play a game like poker right like you probably played poker before and with your friends you probably asked like oh what do you have called me if I raised there you know and that's that's a person trying to do the same kind of like learning from a counter factual that the

**[16:52]** AI is doing okay and if you do that at scale you're going to be able to learn an optimal policy yeah now where the neural nets come in I said like okay if it's in that situation again then it will choose the action that has high regret now the problem is that poker is such a huge game you know I think no limit Texas Hold'em the version that we were playing has 10 to the 161 different decision points which is more than the

**[17:14]** number of atoms in the universe squared that's heads up that's heads up yeah 10 to the 161 you said yeah I mean it depends on the number of chips that you have the stacks and everything but like the version that we were playing was tense to the 161. which I assume would be a somewhat simplified version anyway because the about there's some like step

**[17:33]** function you had for like bets oh no no that's that's I'm saying like we played the the full game you can bet whatever amount you want another thought maybe was constrained in like what it considered for bed sizes but the the person on the other side could bet whatever they wanted yeah I mean 161 plus or minus 10 doesn't matter yeah um and so the way neural Nets help out here is you know you don't have to run into the same exact situation because

**[17:55]** that's never going to happen again the odds of you running into the same exact situation are pretty slim but if you run into a similar situation then you can generalize from other states that you've been in that kind of look like that one and you can say like well these other situations I had high regret for this action and so maybe I should play that action here as well which is the more complex game chess or poker or go or

**[18:18]** poker do you know that is a controversial question okay um I'm gonna it's like somebody screaming on Reddit right now it depends on which subreddit you're on is it chess or is it poker I'm sure like David Silver's gonna get really angry at me yeah I'll say I'm gonna say poker actually and I think for a couple reasons um they're not here to defend themselves so first of all you have the imperfect information aspect and so it's um it we

**[18:43]** can go into that but like once you introduce imperfect information uh things get much more complicated so we should say maybe you can describe what is seen to the players what is not seen uh in the game of Texas Hold'em yeah so Texas Hold'em you get two cards face down that only you see um and so that's the hidden information of the game the other players also all get two cards face down that only they see um and so you have to kind of as you're

**[19:08]** playing reason about like okay what do they think I have what do they have what do they think I think they have that kind of stuff and um that's that's kind of where bluffing comes into play right because the fact that you can Bluff the fact that you can bet with a bad hand and still win is because they don't know what your cards are right and that's the that's the key difference between a perfect information game like poker uh sorry like chess and

**[19:30]** go um and imprint information games like poker this is what trash talk looks like

**[19:39]** the implied statement is the game I solved is much tougher uh but yeah so uh when you're playing I'm just gonna do random questions here so what when you're playing your opponent under imperfect information

**[19:54]** is there some degree to which you're trying to estimate the range of hands that they have or is that not part of the algorithm so how what are the different approaches to the imperfect information game so the

**[20:07]** key thing to understand about why in perfect information makes things difficult is that you have to worry not just about which actions to play but the probability that you're going to play those actions so you think about um rock paper scissors for example rock paper scissors is an imperfect information game um right because you don't know what I'm about to throw I do but yeah usually not yeah yeah and so you can't just say like

**[20:28]** I'm just gonna throw a rock every single time because the other person is going to figure that out and notice a pattern and then suddenly you're going to start losing and so you don't just have to figure out like which action to play you have to figure out the probability that you play it and really importantly the value of an action depends on the probability that you're going to play it so if you're playing Rock every single

**[20:47]** time that value is really low but if you're never playing rock you play Rock like one percent of the time then suddenly the the other person's probably gonna be throwing scissors and when you throw rock the value of that action is going to be really high now you take that to Poker what that means is the value of bluffing for example if you're the kind of person that never Bluffs and you have this reputation as somebody that never Bluffs and suddenly

**[21:11]** you Bluff there's a really good chance that that bluff is going to work and you're gonna make a lot of money on the other hand if you've got a reputation like if they seen you play for a long time and they see oh you're the kind of person that's bluffing all the time when you Bluff they're not going to buy it and they're going to call you down you're going to lose a lot of money and that finding that balance of how often you should be bluffing is uh the

**[21:31]** key challenge of a game of poker and um you contrast that with a game like chess it doesn't matter if you're opening with the Queen's Gambit 10 of the time or 100 of the time the value the expected value is the same so um so that's that's why we need these algorithms that understand not just we

**[21:55]** have to figure out what actions are good but the probabilities we need to get the exact probabilities correct and that's actually when we created the bot labradus libratus means balanced because the algorithm that we designed was designed to find that right balance of how often it should play each action the balance of how often in the key sort of branching is the bluff or not the bluff is that a is that a good crude simplification of the major decision in

**[22:18]** poker it's a good simplification I think that's like the main tension but it's it's not just how often the bluff or not to Bluff it's like how often should you bet in general how often should you what what kind of bet should you make um should you bet big or should you bet small and with which with which hands uh and so this is where the idea of a range comes from because when you are bluffing with a particular hand in a particular

**[22:42]** spot you don't want there to be a pattern for the other person to pick up on you don't want them to figure out oh whenever this person is in this spot they're always bluffing and so you have to reason about okay would I also bet with a good hand in this spot you want to be unpredictable so you have to think about what would I do if I had this different set of cards is there explicit estimation of like a theory of mind that the other person has about you

**[23:08]** or is that just a emergent thing that happens the way that the Bots handle it that are really successful they have an explicit theory of mine so they're explicitly reasoning about what are what's the

**[23:24]** common knowledge belief what does what do you think I have what do I think you have what do you think I think you have um it's explicitly reasoning about that is there multiple U's there so maybe that's jumping ahead to six players but is there a stickiness to the person to so it's an iterative game you're playing the same person there is there's a stickiness to that right you're gathering information as you play it's not every every

**[23:48]** um every hand is in your hand is there um a continuation in terms of estimating what kind of player I'm facing here that's a good question so you could approach the game that way the way that the Bots do it they don't and the way that humans approach it also expert human players the way they approach it is to basically assume that you know my strategy so

**[24:14]** I'm going to try to pick a strategy where even if I were to play it for 10 000 hands and you could figure out exactly what it was you still wouldn't be able to beat it basically what that means is I'm trying to approximate the Nash equilibrium I'm trying to be perfectly balanced because if if I'm playing the national equilibrium even if you know what my strategy is like I said I'm still unbeatable in expectation so so that's what that's what the bot aims

**[24:33]** for and that's actually what a lot of expert poker players aim for as well to start by playing the Nash equilibrium and then maybe if they spot weaknesses in the way you're playing then they can deviate a little bit to take advantage of that they aim to be unbeatable in expectation okay so who's the greatest poker player of all time and why is it Phil Hellmuth so this is for Phil uh so he's known um at least in part for maybe playing

**[24:59]** sub-optimally and he still wins a lot it's a bit chaotic so maybe can you speak from an AI perspective about the genius of his Madness or The Madness of his genius so playing sub optimally playing chaotically

**[25:19]** um as a way to make it hard to pin down about what your strategy is so okay the thing that I should explain first of all was like Nash equilibrium it doesn't mean that it's predictable the whole point of it is that you're trying to be unpredictable now I think when somebody like Phil Hellmuth might be really successful is not in being unpredictable but in being able to um take advantage of the other player and figure out where they're being

**[25:43]** predictable or guiding the other player into thinking that you have certain weaknesses and then and then understanding how they're going to change their behavior they're going to deviate from a Nash equilibrium style of play to try to take advantage of those perceived weaknesses and then counter exploit them so you kind of get into the Mind Games there so you think about these heads up poker as a dance between two agents I guess are you playing the

**[26:06]** cards are you playing the the player so this this gets down to a big argument in the poker community and the academic Community for a long time there was this debate of like what's called GTO Game Theory optimal poker or exploitative play and um up until about like 2017 when we did the broadest match I think actually exploitative play had the advantage a lot of people were saying like oh this whole idea of Game Theory it's just

**[26:31]** nonsense and if you really want to make money you got to like look into the other person's eyes and read their soul and figure out what cards they have but what happened was people started adopting the game theory optimal strategy um and they were making good money and they weren't trying to adapt so much to the other player they were just trying to play the national equilibrium and then what really solidified it I think

**[26:53]** was the broadest the broadest match where we played our bot against four top heads up no limit Hold'em poker players and the bot wasn't trying to adapt to them it wasn't trying to exploit them it wasn't trying to do these Mind Games it was just trying to approximate the Nash equilibrium and it crushed them I think you know it we've we're playing for 50 100 blinds and over the course of about 120 000 hands it made close to two million

**[27:19]** dollars 120 000 hands 120 000 hands against humans yeah and this was this was fake money to be clear so there was real money at stake there was 200 000 first of all all money is fake but um that's that's that's a different conversation um we give it meaning uh it's an it's a it's a phenomena that gets meaning from our uh complex psychology as a human civilization um it's emerging from the collective intelligence of the human species but

**[27:44]** that's not what you mean you mean like there's literally you can't you can't buy stuff with it okay can you actually uh step back and take me through that um competition yeah okay so

**[27:57]** when I was in grad school um there was this thing called the annual computer poker competition where every year all the different research Labs that were working on AI for poker would get together they would make a bot they would play them against each other uh and we made a bot that actually won the um 2014 competition the 2016 competition uh and so we decided we're gonna take this bot build on it and play against Real top professional heads up

**[28:20]** no limit Texas hold 'em poker players so we invited four of the world's best players in this specialty and we challenge them to 120 000 hands of poker over the course of 20 days um and we had 200 000 200 000 in prize money at stake where it would basically be divided among them depending on how well they did relative to each other so we wanted to have some incentive for them to play their best did you have a confidence

**[28:47]** 2014-16 that this is even possible how much doubt was there so and we did a competition actually in 2015 where we also played against professional poker players and the bot lost by by a pretty sizable margin actually now there were some big improvements from 2015 to 2017. and so can you speak to the improvements is it computational nature is it the algorithm the the methods it was it was really an algorithmic approach that was

**[29:11]** the difference so 2015 it was much more focused on trying to come up with a strategy up front like trying to solve the entire game of poker like and then just have a lookup table where you're saying like oh I'm in this situation what's the strategy um the approach that we took in 2017 was much more search based it was trying to say okay well let me in real time try to compute a much better strategy than what I had pre-computed by playing against

**[29:39]** myself during self-play what is the search space for poker what are you searching over

**[29:49]** what's that look like there's different actions like raising calling yeah what are the actions um is it just a search over actions so in a game like chess the the search is like okay I'm in this chess position and I can like you know move these different pieces and see where things end up in poker what you're searching over is the actions you can take for your hand the probabilities that you take those actions and then also the probabilities

**[30:14]** that you take other actions with other hands that you might have um and and that's kind of like a hard to wrap your head around like why are you searching over these like other hands that you might have and like trying to figure out what you would do with those hands um and the idea is is again you you wanna you wanna always be balanced and unpredictable and so if you're a search algorithm that's saying like oh I want

**[30:37]** to raise with this hand well in order to know whether that's a good action like let's say it's a bluff you know let's say you have a bad hand and you're saying like oh I I think I should be betting here with this really bad hand and bluffing well that all that's only a good action if you're also betting with a strong hand otherwise it's an obvious Bluff so if your action in some sense maximizes your unpredictability so that action could be

**[31:00]** mapped by your opponent to a lot of different hands then that's a good action basically what you want to do is put your opponent into a tough spot so you want them to always have some doubt like should I call here should I fold here and if you are raising in the appropriate balance between Bluffs and good hands then you're putting them into that tough spot and so that's what we're trying to do we're always trying to search for a strategy that would put the

**[31:23]** opponent into a difficult position can you give a metric that you're trying to maximize or minimize does this have to do with the regret thing what we're talking about in terms of putting your opponent in a maximally tough spot yeah ultimately what you're trying to maximize is your expected winnings like your expected value the amount of money that you're going to walk away from assuming that your opponent was playing

**[31:43]** optimally in response so you're going to assume that your opponent is is also playing um like as as well as possible Nash equilibrium approach because if they're not then you're just going to make more money right like anything that deviates like by definition the national equilibrium is the strategy that does the best in expectation and so if you're deviating from that then you're just they're going to lose money and since

**[32:08]** it's a two player zero-sum game that means you're gonna make money so there's not an explicit like objective function that maximizes the toughness of the spot they're put in you're always this is not from like a self-play reinforcement learning perspective you're just trying to maximize winnings and the rest is implicit that's right yeah so we're what we're actually trying to maximize is the expected value given that the opponent is playing optimally

**[32:32]** in response to us now in practice what that ends up looking like is it's putting the opponent into difficult situations where there's no obvious decision to be made so the the system doesn't know anything about the difficulty of the situation not at all it doesn't care okay yeah all right my head was getting excited whenever I was making the other the opponent's sweat okay so you're in 2015 you didn't do as well so what's the journey from that to

**[32:54]** a system that in your mind could have a chance so 2015 we we got we got beat pretty badly and we actually learned a lot from that competition and in particular you know what became clear to me is that the way the humans were approaching the game was very different from how the bot was approaching the game the bot would not be doing search it would just be trying to compute you know it would do like months of self-play it would just be playing

**[33:20]** against itself for months but then when it's actually playing the game it would just act instantly um and the humans when they're in a tough spot they would sit there and think for sometimes even like five minutes about whether they're going to call or fold a hand um and it became clear to me that that's there's a good chance that that's what that's what's missing from our bot so I actually did some um initial experiments to try to figure

**[33:44]** out how much of a difference this is actually make and the difference was huge as a signal to the human player how long you took to think no no I'm not saying that there were any timing tells I was saying when the human like the bot would always act instantly it wouldn't try to come up with a better strategy in real time um over what it had precomputed during training whereas the human like they have all this intuition about how to

**[34:05]** play but they're also in real time leveraging their ability to think just

**[34:12]** to search to plan um and coming up with an even better strategy than what their intuition would say so you're saying that there's you're doing that's what you mean by you're doing search also you have an you have a intuition and searched on top of that looking for a better solution yeah that's that's what I mean by search that um instead of acting instantly you know a neural net usually gives you a response in like 100 milliseconds or

**[34:35]** something it depends on the size of the of the net but if you can leverage extra computational resources you can't possibly get a much better outcome and we did some experiments in

**[34:49]** small scale versions of Poker and what we what we found was that if you do a little bit of search even just a little bit it was the equivalent of making your you know your pre-computed

**[35:03]** strategy like you could kind of think it as your neural net a thousand times bigger with just a little bit of search and it just like blew away all of the research that we had been working on and trying to like scale up this like pre-computed solution it was dwarfed by the benefit that we got from search can you just Linger on what you mean by search here you're searching over a space of actions for your hand and for other hands how

**[35:25]** are you selecting the other hands to search over and so yeah randomly no it's all the other hands that you could have so when you're playing No Limit taxes hold on you've got two face down cards and so that's 52 choose two one thousand three hundred twenty six different combinations now that's actually a little bit lower because there's Facebook cards in the middle and so you can eliminate those as well but you're looking at like around a thousand

**[35:48]** different possible hands that you can have and so when we're doing when the bot's doing search It's thinking explicitly there are these thousand different hands that I could have there are these thousand different hands that you could have let me try to figure out what would it be a better strategy than what I've pre-computed for these hands and your hands Okay so that search how do you fuse that with

**[36:14]** what the neural net is telling you or what the the the train system is telling you yeah so you kind of like where the train system comes in is is the value um at the end so there's um you only look so far ahead you look like maybe you know one round ahead so if you're on the Flop you're looking to the start of the turn um and at that point you can use the pre-computed solution to figure out what are what's the value here of like of

**[36:40]** this strategy is it of a single action essentially in that spot you're getting a value or is it the value of the entire series of actions well it's kind of both um because you're trying to maximize the value for the hand that you have but in the process in order to maximize the value of the hand that you have you have to figure out what would I be doing with all these other hands as well okay but you are you in the search always going

**[37:05]** to the end of the game in liberatis we did uh so we only use search starting on the turn and then we searched all the way to the end of the game the turn the river uh can we take it through the terminology yeah there's four rounds of Poker so there's the pre-flop the Flop the turn and the river uh and so we would start doing search halfway through the game now the first half of the game that was all pre-computed it would just

**[37:32]** act instantly and then when it got to at the halfway point then it would always search to the end of the game now we later improved this so wouldn't have to search all the way to the end of the game it would actually search um just a few moves ahead um but that that came later and that drastically reduced the num the amount of computational resources that we needed but the moves because you can keep betting on top of each other that's

**[37:52]** what you mean by moves so like that's where you don't just get one bet per Turner poker you can have multiple arbitrary number of bets right right I'm trying to think like I'm gonna bet and then what are you gonna do in response are you gonna raise me are you going to call and then if you raise what should I do so it's reasoning about that whole process up until the end of the game in the case of liberatis so for liberatis

**[38:14]** what's the the most number of re-racists have you ever seen uh you probably cap out at like five or something because at that point you're basically all in you know I mean is there like uh interesting patterns like that that you've seen that the game does like you you'll have like Alpha zero doing way more sacrifices than humans usually do is there something like the bratis was constantly re-raising or something like that even noticed there

**[38:41]** was there was something really interesting that we observed with the broadest um so humans when they're playing poker they usually size their bets relative to the size of the pot so you know if the pot has a hundred dollars in there maybe you bet like 75 or somewhere around there somewhere between like 50 and 100 um and with libratus we gave it the option to basically bet whatever it wanted it was actually really easy for

**[39:04]** us to say like oh if you want you can bet like 10 times the pot and we didn't think it would actually do that it was just like why not give it the option and then during the competition it actually started doing this and by the way this is like a very last minute decision on our part to add this option and so we did not we did not think the bot would would do this and uh I was actually kind of worried when it did start to do this

**[39:25]** like oh is this is a problem like humans don't do this like is it screwing up um but it would put the humans into really difficult spots when it would do that because you know you can imagine like you have the second best hand that's possible given the board and you're thinking like oh you're in a really great spot here and suddenly the bot bets twenty thousand dollars into a you know a thousand dollar pot and and it's

**[39:45]** basically saying like I have the best hand or I'm bluffing and you having the

**[39:53]** second best hand like now you get a really tough choice to make and so the humans would sometimes think like five or ten minutes about like what do you do should I call should I fold and um and when I saw the humans like really struggling with that decision like that's when I realized like oh actually this is maybe a good thing to do after all and of course the system doesn't know that it's making again like we said that it's putting them in a tough spot

**[40:14]** it's it's it's just that's part of the optimal the game theory optimal right from the Bots perspective it's just it's just doing the thing that's going to make it the most money um and the fact that it's putting the humans in a difficult spot like that's just um you know a side effect of that and this was I think the the one thing I mean there were a few things that the humans walked away from but this was the the number one thing that the humans

**[40:38]** walked away from the competition saying like we need to start doing this um and now these over bats what are called over bets have become really common in high level poker play have you ever talked to like somebody like Danny on the ground about this he seems to be a student of the game I did actually have a conversation with Daniel degrania once yeah I was uh I was visiting the Isle of Man to talk to Poker Stars about

**[40:58]** AI um and Daniel legrandi was there when we had dinner together with uh some other people and um yeah he was really interested in it he mentioned that he was like you know excited about like learning from these AIS um so he wasn't scared he was excited he was excited and uh and he all he honestly he wanted to play against the bot he thought he thought he had a decent chance of beating it um I I think he's you know this was like several years ago and I

**[41:25]** think it was like not as clear to everybody that you know the AIS were taking over I think now people recognize that like if you're playing against uh a bot there's like no chance that you have in a game like Pokemon so consistently the Bots will win the Bots have heads up and in in other variants too so multi multi six player Texas Hold'em No Limit taxes hold them as the Bots win yeah that's the case so I think there's some

**[41:52]** debate about like is it true for every single variant of Poker I think I think for every single variant of Poker if somebody really put in the effort they can make an AI that would beat all humans at it um we've focused on the most popular variants so heads up no limit Texas Hold'em and then we followed it up with um with uh six player poker as well where we managed to uh make a bot that beat expert human players and I think

**[42:14]** even there now uh it's pretty clear that humans don't stand a chance see I would love to hook up an AI system that looks at EEG like how like actually tries to optimize the toughness of the spot it puts a human in and I I would I would love to see how different is that from the game theory optimal so you try to maximize the heart rate of the human player like the freaking out over a long period of time I wonder if there's going to be

**[42:42]** different strategies that emerge uh that are close in terms of Effectiveness because something tells me you could still be um achieved superhuman level performance by just making people sweat I feel like that there's a good chance that that is the case yeah if you're able to see like that it's like it's like a decent proxy for score right right um and this is actually like the the common poker wisdom when they're telling where they're teaching players

**[43:10]** before the robots and they were trying to teach people how to play poker they would say like the key to the game is to put your opponent into difficult spots it's a good um a good estimate for if you're making the right decision so what else can you say about the fundamental role of search in poker and maybe if you

**[43:28]** can also relate it to chess and go in these games um what's the role of search to solve in these games yeah I think a lot of people under this is true for the general public and I think it's true for the AI Community a lot of people underestimate the importance of search for these kinds of game AI results um an example of this is uh TD Gammon that came out in 1992 this was the the first real instance of a neural net being used in a game AI it's a landmark

**[43:55]** achievement it was actually the inspiration for Alpha zero and it used search it used two-ply search to figure out its next move you got deep blue there he was very heavily focused on search um looking many many moves ahead farther than any human could and that was key for why it won and then even with something like alphago I mean alphago is commonly hailed as a landmark achievement for neural Nets and it is but there's also this huge component of

**[44:24]** search Monte Carlo tree search to alphago that was key absolutely essential for the AI to be able to beat top humans um I think a good example of this is you look at the latest versions of alpha of alphago like it was called Alpha zero um and there's this metric called ELO rating where you can compare different humans and you can compare Bots to humans now a top human player is around 3600 ELO maybe a little bit higher now

**[44:51]** um Alpha zero the strongest version is around 5200 ELO but if you take out the search that's being done at test time and by the way what I mean by search is the planning ahead the thinking of like oh if I move my if I place the stone here and then he does this and then you look like five moves ahead and you see like what the board state looks like um that's what I mean by search if you take out the search that's done during

**[45:17]** the game the ELO rating drops to around three thousand so even today what seven years after alphago if you take out the Monte Carlo research that's being done at one playing against the human the Bots are not superhuman nobody has made a raw neural net that is superhuman and go that's worth lingering on that's that's quite profound so without search that just means looking at the next move and saying this is the best move so

**[45:47]** having a function that estimates accurately what the best move is that's right without search yeah and all these Bots they have the what's called a policy Network where it will tell you this is what the neural net thinks is the next best move um and it's kind of like a the intuition that a human has you know the human looks at the board and and any uh go or chess master will be able to tell you like oh instantly here's what I think

**[46:14]** the right move is um and the bot is able to do the same thing but just like how a human Grandmaster can make a better decision if they have more time to think when you add on this Monte Carlo tree search the bot is able to make a better decision yeah I mean of course a human is doing something like searching their brain but it's not I hesitate to draw a hard line but it's not like uh Monte Carlo tree search it's more like

**[46:42]** sequential language model generation so

**[46:47]** it's like a different it's a the neural network is doing the searching and I wonder what the human brain is doing in terms of searching because you're doing that like computation the human is Computing they have intuition they've got they have a really strong ability to estimate you know amongst the top players of what is a good and not position without calculating all the details but they're still doing search in their

**[47:08]** head but it's a different kind of search have you ever thought about like what is the difference between the human the search that the human is performing versus what computers are doing I have thought a lot about that and I think it's a really important question so the AI in Alpha and Alphas in alphago or any of these go AIS they're all doing Monte College research which is a particular kind of search and it it's actually a symbolic

**[47:32]** tabular search it uses the neural net to guide its search but it isn't actually like full full-on neural net now that kind of search is very successful in these kinds of like perfect information board games like chess and go but if you take it to a game like poker for example it doesn't work it can't it can't understand the concept of hidden information it doesn't understand the balance that you have to strike between like the amount that

**[47:58]** you're raising versus the amount that you're calling and in every one of these games you see a different kind of search and the human brain is able to plan for all these different games in a very general way now I think that's one thing that we're missing from AI today and I think it's a really important missing piece the ability to plan and reason more generally across a wide variety of different settings in a way where the general reasoning

**[48:23]** makes you better at each one of the games not worse yeah so you can kind of think of it as like neural Nets today they'll give you like Transformers for example or super General but you know they'll give you it'll output an answer in like 100 milliseconds and if you tell it like oh you've got five minutes to give you a decision you know feel free to take more time to make a better decision it's not gonna know what to do

**[48:44]** with that um but a human if you're playing a game like chess they're going to give you a very different answer depending on if you say oh you've got 100 milliseconds or you've got five minutes yeah there I mean that people have started using right Transformers the language models like the in an iterative way that does improve the answer or like showing the work the kind of kind of idea yeah they got this thing called Chain of Thought reasoning and that's I

**[49:09]** think um super promising right yeah I think and I think it's a good step in the right direction um I I would kind of like say it's similar to Monte Carlo rollouts in in a game like chess there's a kind of search that you can do where you're saying like I'm Gonna Roll Out My intuition and see like without really thinking you know what are the better decisions I can make farther down the path um what would I do if I just acted

**[49:30]** according to intuition for the next 10 moves um and that gets you an improvement but I think that there's much uh much richer kinds of of planning that we could do so when the broadest actually beat the poker plays what did I feel like what was that I mean actually on that day what were you feeling like were you were you nervous

**[49:53]** I mean Poco was one of the games that he thought like is not going to be solvable because it's the human factor so at least in the narratives we tell ourselves the human factor so fundamental to the game of poker yeah the liberatis competition was super stressful for me um also I mean I was working on this like basically continuously for a year leading up to the competition I mean for me it became like very clear like okay

**[50:15]** this is the search technique this is the approach that we need and then I spent a year working on this pretty much like non-stop oh can we actually get into details like what programming language is it written in what's some interesting uh implementation details that are like

**[50:31]** fun slash painful yeah so one of the interesting things about liberatis is that we had no idea what the bar was to actually beat top humans yeah we could play against like our prior Bots and that kind of gives us some sense of like are we making progress are we going in the right direction uh but we had no idea like what the bar actually was and so we threw a huge amount of resources at trying to make the strongest bot

**[50:50]** possible so we use C plus plus it was parallelized we were using I think like a thousand CPUs uh maybe maybe more actually um and you know today that sounds like nothing but for a grad student back in 2016 that was a huge amount of resources but still a lot for even any gratitude today it's still tough to to get or even to allow yourself to think in that in terms of scale at CMU at MIT anything like that yeah and you know

**[51:17]** talking about terabytes of memory um so it's a very paralyzed um and it had to be very fast too because the more games that you could simulate uh the stronger the bot would be so is there some like John Carmack Style like efficiencies you have to come up with like an efficient way to represent a hand all that kind of stuff there were all sorts of optimizations that I had to make to try to get this thing to run as fast as possible they were like how do

**[51:43]** you minimize the latency how do you like you know package things together so that like you minimize the amount of communication between the different nodes um how do you like optimize the algorithm so that you can you know try to squeeze out more and more from the game that you're actually playing all these kinds of different decisions that that I you know had to make uh just a fun question what what id did you use what uh for for C plus plus

**[52:07]** I think I used a visual studio actually yeah okay yeah is that still carried through to today vs code is is what I use today it seems like it's pretty the community basically converged on Okay cool so you got you got this super optimized C plus plus system and then you show up to the day of competition yeah humans versus machine

**[52:32]** um how did it feel throughout the day super stressful um I mean I thought going into it that we had like a 50 50 chance because basically I thought if if they play in a totally normal style I think we'll squeak out a win but there's always a chance that they can find some weakness in the bot and if they do and we're playing like for 20 days 120 000 hands of poker they have a lot of time to find weaknesses in the system and if they do

**[52:54]** we're gonna get crushed and that's actually what happened in the previous competition um the humans you know they started out it wasn't like a they were winning from the start but then they found these weaknesses that they could take advantage of and for the next they know like 10 days they were just just crushing the bot stealing money from it what were the weaknesses they found like maybe over betting was effective that

**[53:14]** kind of stuff so certain betting strategies worked what they found is yeah over betting like betting certain amounts the bot would have a lot of trouble dealing with those sizes and then also um when it the bot got into really difficult all-in situations it wasn't able to because it wasn't doing search it had to Clump different hands together and it wouldn't it would treat them identically yeah um and so it wouldn't be able to distinguish you know like

**[53:41]** having a king High flush versus an ace high flush and in some situations that really matters a lot and so they could put the bot into those situations and then the bot would would just bleed money clever humans yeah okay so I didn't realize it was over 20 days so

**[53:59]** um what were the humans like over those 20 days and what was the bot like so we had set up the competition you know like I said there was two hundred thousand dollars in prize money and they would get paid a fraction of that depending on how well they did relative to each other yeah so I was kind of hoping that they wouldn't work together to try to find weaknesses in the bot but they entered the competition with their like number

**[54:19]** one objective being to beat the bot and they didn't care about like individual Glory they were like we're all going to work as a team to try to take down the spot yeah and so they immediately started comparing notes what they would do is they would coordinate looking at

**[54:35]** different parts of the strategy to try to try to you know find out weaknesses um and then at the end of the day we actually sent them a log of all the hands that were played and what cards the bot had on each of those hands oh wow yeah that's that's gutsy yeah it was honestly and I'm not sure why we did that in retrospect but um I mean I'm glad we did it because we ended up winning anyway but that if if you've ever played poker before like that is

**[54:56]** golden information I mean to know usually when you play poker you see about a third of the hands to Showdown um and to just hand them all the cards that the bot had on every single hand that was um just just a gold mine for them yeah and so then they would review the hands and try to see like okay could they find patterns in the bot the weaknesses and could they then then they would coordinate and study together and try to

**[55:19]** figure out okay now this person's gonna explore this part of the strategy for weaknesses this person's gonna explore this part of the strategy for weaknesses it's a kind of psychological warfare showing in the hands yeah um I mean I'm sure you didn't think of it that way but like doing that means you're confident in the possibility to win well that's that's one way of putting it I wasn't uh super confident yeah so you know going in like I said I think I

**[55:42]** had like 50 50 odds on us winning the when we actually when we announced the competition the poker Community decided to gamble on who would win and their initial odds against us were like four to one they were really convinced that the humans were gonna pull out a win um the bot ended up winning for three days straight and even then after three days the betting odds were still just 50 50. um and then at that point it started to

**[56:07]** look like the humans were coming back um they started to like you know but but poker is a very high variance game um and I think what happened is like they thought that they spotted some weaknesses that weren't actually there and then around day eight it was just very clear that they were getting absolutely crushed um and and from that point I mean for for a while there I was super stressed out thinking like oh my God the humans

**[56:31]** are coming back and we're just they've found weaknesses and now we're just gonna lose the whole thing but no it ended up going in the other direction and the bot ended up like crushing them in the long run how did it uh feel at the end like as a human being what it as a person who loves appreciates the beauty of the Game of Poker and the person who appreciates the beauty of AI is there did you feel a certain kind of way about it

**[56:57]** uh I felt a lot of a lot of things man um I mean at that point in my life I had spent five years working on this project and um it was a huge sense of accomplishment I mean to spend five years working on something and finally see it succeed um yeah I wouldn't trade that for anything in the world yeah because it's uh that's a real Benchmark it's not like uh getting us some percent accuracy and

**[57:22]** a data set this is like real this is real world it's it's just a game but it's also a game it means a lot to a lot of people and this is humans doing their best to beat the machine so this is a real Benchmark unlike anything else yeah and I mean this is this is what I have been dreaming about since I was like 16 playing poker you know with my friends in high school the idea that you could find a strategy um you know approximate the national

**[57:46]** equilibrium be able to beat all the poker players in the world with it you know so to actually see that come to fruition and be realized uh that was is kind of magical yeah especially money is on the line too it's a different it's different than chess and that aspect like people get that's why you want to look at Betty Marcus if you want to actually understand what people really think in the same sense poker it's really high stakes because

**[58:12]** it's money and to solve that game that's that's an amazing accomplishment so the leap from that to multi-way six player poker what's how

**[58:25]** difficult does that jump and what are some interesting differences between heads up poker and and multi-way poker yeah so I mentioned you know Nash equilibrium and two player zero-sum games if you play that strategy you are guaranteed to not lose an expectation no matter what your opponent does now once you go to six player poker you're no longer playing a two player zero-sum game and so there was a lot of debate among the academic community and among

**[58:46]** the poker Community about how well these techniques would extend beyond just two-player heads-up poker now

**[58:55]** what I have come to realize is that um the techniques actually I thought really would extend to six player poker because even though in theory they don't give you these guarantees outside of two player zero some games in practice it still gives you a really strong strategy now there were a lot of complications that would come up with six player poker besides like the game theoretic aspect I mean for one the game is Just

**[59:18]** exponentially larger

**[59:22]** um so the main thing that allowed us to go from two player to six player was the idea of depth limited search so I said before like you know we would do search we would plan out the bot would plan out like what what it's going to do next and for the next several moves and in liberatis that search was done extending all the way to the end of the game so it would have to start um it from from the turn onwards like

**[59:47]** looking maybe 10 moves ahead um it would have to figure out what it was doing for all those moves now when you get to six player poker it can't do that exhaustive search anymore because the game is just way too large um but by only having to look a few moves ahead and then stopping there and substituting a Value Estimate of like how good is that strategy at that point then we're able to do a much more scalable form of search

**[1:00:14]** is there something cool looking at the paper right now is there something cool in the paper in terms of Graphics a game tree Traverse of via Monte Carlo I think if you go down a bit uh uh figure one an example of equilibrium selection problem ooh so yeah uh what do we know about equilibria one is there's multiple players so when you go outside of two players you're a sum so a Nash equilibrium is a set of strategies like

**[1:00:38]** one strategy for each player where no player has an incentive to switch to a different strategy um and so you can kind of think of it as like imagine you have a game where there's a ring that's actually the visual here you got a ring and the object of the game is to be as far away from the other players as possible there's an ash equilibrium is for all the players to be spaced equally apart around this ring but there's infinitely many different

**[1:01:04]** Nash equilibria right there's infinitely many ways to space four dots along a ring And if every single player independently computes a Nash equilibrium then there's no guarantee that the joint strategy that they're all playing is going to result is going to be in Ash equilibrium there they're just going to be like random dots scattered along this ring rather than four coordinated dots being equally spaced apart is it possible to sort of optimally do this

**[1:01:29]** kind of selection to do the selection about

**[1:01:35]** um of the equilibrium you're chasing so is there like a meta problem to be solved here so the meta problem is in some sense um how do you how do you understand the national equilibria that the other players are going to play um and and even if you do that again there's no guarantee that you're going to win so you know if you're playing uh if you're playing risk like I said and and all the other players decide to team up against you You're Gonna Lose

**[1:01:59]** Nash equilibrium doesn't help you there and so there was this big debate about whether Nash equilibrium and all these techniques that compute it are even useful once you go outside of two player zero some games now I think for many games there is a valid criticism here and I think when we talk about when we go to something like diplomacy we run into this issue that the approach of trying to approximate a Nash equilibrium

**[1:02:23]** doesn't really work anymore but it turns out that in six player poker um because six player poker is such an adversarial game um where none of the players really try to work with each other the techniques that were used in two-player poker to try to approximate an equilibrium those still end up working in practice in in six player poker there's some deep way in which six player poker is just a bunch of heads up poker like

**[1:02:49]** games in one it's like uh it's like embedded in it so the competitiveness um is more fundamental to Poker than the cooperation right yeah poker is just such an adversarial game there's no real cooperation in fact you're not even allowed to cooperate in poker it's considered collusion it's against the rules um and so for that reason the techniques end up working really well and I think that's true more more broadly in extremely adverse serial games in

**[1:03:16]** general but that's sort of in practice versus being able to prove something that's right nobody has a proof that that's the case and it could be that that six player poker belongs to some class of games where a pro approximating an Azure equilibrium through self-play provably works well um and you know there are other classes of games Beyond just two player Zero Sum where this is proven to work well so there are these you know kinds of games

**[1:03:41]** called potential games which I won't go into it's kind of like a complicated concept but um there are classes of games where uh this approach to approximating an ash equilibrium is proven to work well now six player poker is not known to belong to one of those classes but it is possible that there is some classic games where it either provably performs well or provably performs not that badly so what are some interesting things

**[1:04:04]** about uh pluribus that was able to achieve human level performance on this or superhuman level performance on the six player version of Poker I personally I think the most interesting interesting thing about pluribus is that it was so much cheaper than libratus I mean libratus if you had to put a price tag on on the computational resources that went into it I would say the final training run took about a hundred thousand dollars

**[1:04:29]** you go to pluribus the final training run would cost like less than 150 on AWS is this normalized to computational

**[1:04:40]** inflation so meaning uh this is is this just does this just have to do with the fact that pluribus was trained like a year later no no it's not it's I mean first of all like yeah Computing resources are are getting cheaper every day and like but you're not going to see a thousand-fold decrease in the computational resources over two years um or even anywhere close to that the the real Improvement was algorithmic improvements and in particular the

**[1:05:04]** ability to do depth limited search so it does depth limited search also work for libratus yeah yes so where this

**[1:05:14]** deploymented search came from is you know I I developed this technique and um ran it on two-player poker first and that reduced the computational resources needed to make an AI that was superhuman from you know a hundred thousand dollars for the broadest to something you could train on your laptop what do you learn from that

**[1:05:34]** um from that discovery what I would take away from that is that algorithmic improvements really do matter how would you describe the more General case of limited Dev search so it's basically constraining the scale a temporal or in some other way of the computation you're doing in some clever way so like with like how else can you significantly constrain computation right well I think the idea is that we want to be able to leverage search as much as

**[1:06:02]** possible and the way that we were doing it in liberatis required us to search all the way to the end of the game now if you're playing a game like chess the idea that you're going to search always to the end of the game is kind of unimaginable right like there's just so many situations where you just won't be able to use search in that case or the cost would be um you know prohibitive and this technique allowed us to

**[1:06:24]** leverage search and without having to pay such a huge computational cost for it and be able to apply it more broadly so to what degree did you use neural nets for uh libratus and pluribus and more generally what role do neural Nets have to play in um in super human level performance in poker so we actually did not use neural Nets at all for libratus or pluribus and a lot of people found this surprising back in 2017 I think they

**[1:06:51]** found it surprising today um that we were able to do this without using any neural Nets um and I think the reason for that I mean I think neural Nets are um incredibly powerful and the techniques that are used today even for poker AIS do rely uh quite heavily on neural Nets um but it wasn't the main challenge for poker like I think what neural Nets are really good for if you're in a situation where finding features for a value

**[1:07:18]** function is really difficult then neural Nets are really powerful and this was the problem in go right like the problem and go was that or the final problem in go at least was that nobody had a good way of looking at a board and figuring out who was winning or describing um through a simple algorithm who was winning or losing and so there neural Nets were super helpful because you could just feed in a ton of different board positions into

**[1:07:44]** this neural net and it would be able to predict then who was winning or losing but in poker the features weren't the challenge the the challenge was how do you design a scalable algorithm that would allow you to find this balance strategy that would understand that you have to Bluff with the right probability so can that be somehow incorporated into the value function this

**[1:08:11]** the complexity of polka that you've described yeah so the way the value functions work in like the latest and greatest poker AIS they do use neural nets for the value function the way it's done is is very different from how it's done in a game like chess or go because in poker you have to reason about beliefs and so the value of a state

**[1:08:34]** depends on the beliefs that players have about what the different cards are like if you have pocket aces then whether

**[1:08:43]** that's a really really good hand or just an okay hand depends on whether you know I have pocket aces where like if you know that I have pocket aces then if I bet you're going to fold immediately but if you think that I have a really bad hand then I could bet with pocket aces and make a ton of money so the value function in poker these days takes the beliefs as an input which is very different from like how how chess and go AIS work

**[1:09:07]** so as a person who appreciates the game uh who do you think is the greatest poker player of all time that's a that's a tough question um Can an AI help answer that question can you can actually add analyze the quality of play right so the AHS engines can can give estimates of the quality of play right

**[1:09:32]** um I wonder if there's a is there an ELO rating type of system for poker I suppose you could but there's just not enough you would have to play a lot of games right a very large number of games like more than you would in chess the deterministic game makes it easier to estimate yellow I think I think it is much harder to estimate something like ELO rating in poker I think it's doable the problem is that the game is very high variants so

**[1:09:55]** you could play you could be profitable in poker for a year and you could actually be a bad player just because the variance is so high I mean you've got top professional poker players that would lose for a year just because they're on a really bad um bad streak so yeah so for ELO you have to have a nice clean way of saying if player a played player B and a B's B that says something that's a signal in poker it's a very noisy signal

**[1:10:22]** it's a very noisy signal now there is a signal there and so you could do this this calculation it would just be much harder um but the same way that AIS have now taken over chess and you know all the top professional chess players train with with AIS the same is true for poker the game has become a very computational

**[1:10:46]** um people trained with AIS to try to find out where they're making mistakes try to learn from the AIS to improve their strategy so

**[1:10:54]** now yeah so the game has been revolutionized in the past five years by by the development of AI in this sport the skill with which you avoided the question of the greatest of all time was impressive so my feeling is that it's a difficult it's a difficult question because just like in chess where you

**[1:11:11]** can't really compare Magnus Carlson today to Gary Kasparov um because the game has evolved so much um the poker players today are so far beyond the the skills of like people that were playing even 10 or 20 years ago um so you look at the kinds of like All-Stars that were on ESPN at like the height of the poker boom pretty much all those players are actually not that good at the game today at least at least the the strategy

**[1:11:36]** aspect I mean there might be still be good at like reading the player at the other side of the table and trying to figure out like are they bluffing or not but in terms of the actual like computational strategy of the game um a lot of them have really struggled to keep up with that development now so for that reason I'll give an answer and I'm gonna say Daniel negranio who you actually had on the podcast recently I saw was a great episode and I love

**[1:12:00]** this so much and Phil's gonna hate this so much and I'm gonna give him I'm gonna give him credit because he is one of the few like old school really strong players that have kept up with the development of AI so he is trying to he's constantly studying the the game theory optimal way of playing exactly yeah and I think a lot of a lot of the old school poker players are just kind of given up on that aspect and and I got

**[1:12:23]** to give them the ground you credit for for keeping up with all the developments that are happening in the sport yeah it's fascinating to watch it's fascinating to watch where it's headed um yeah so there you go some love for Daniel quick pause bathroom break yeah let's do it let's go from poker to diplomacy what is at a high level the game of diplomacy yeah so I talked a lot about two player zero some games and what's interesting

**[1:12:51]** about diplomacy is that it's very different from these like adversarial uh

**[1:12:59]** games like chess go poker even Starcraft and DOTA diplomacy has a much bigger Cooperative element to it it's a seven player game it was actually created in the 50s um and it takes place uh before World War one it's like a map of Europe with seven Great Powers um and they're all trying to form alliances with each other there's a lot of negotiation going on um and so the whole focus of the game is on forming alliances with the other players

**[1:13:27]** to take on the other players England Germany Russia turkey Austria Hungary

**[1:13:33]** Italy and France that's right yeah so the way the game works is on each turn you spend about you know five to fifteen minutes talking to the other players in privates and you make all sorts of deals with them you say like hey let's work together um you know let's team up against this other player because the only way that you can make progress is by working with somebody else against the others um and then after that negotiation

**[1:13:58]** period is done all the players simultaneously submit their moves and

**[1:14:05]** they're all executed at the same time and so you can tell people like hey I'm going to support you this turn um but then you don't follow through with it and they're only going to figure that out once they see the moves being read off how much of it is natural language like written actual text how

**[1:14:21]** much is like uh you're actually saying phrases that are structured so there's different ways to play the game you know you can play it in person and in that case it's all natural language freeform communication there's no constraints on the kinds of deals that you can make the kinds of things that you can discuss um it can also play it online so you can you know send along emails back and forth you can play it like live online

**[1:14:41]** or over voice chat but the the focus the important thing to understand is that this is unstructured communication you can say whatever you want um you can make any sorts of deals that you want and everything is done privately so it's not like you're all around the board together having a conversation you're grabbing somebody going off into a corner and conspiring behind everybody else's back about what you're planning and uh there's no limit

**[1:15:06]** in theory to the conversation you can have directly with one person that's right you can make all sorts of you can talk about anything you could say like hey let's have a long-term alliance against this guy you can say like hey can you support me this turn and in return I'll do this other thing for you next turn or um you know yeah just you can talk about like what you talked about with somebody else and gossip about like what they're planning

**[1:15:28]** um the way that I would describe the game is that it's kind of like a mix between risk poker and the TV show Survivor there's like this big element of like trying to um yeah there's a big social element and the best way that I would describe the game is that it's really a game about people rather than the pieces so risk because it is a map it's kind of war game like

**[1:15:55]** uh poker because there's a game theory component that's very kind of strategic so you could convert it into an artificial intelligence problem and then survive it because of the social component that's a strong social component I saw that somebody said online that the internet version of the game has this quality of that is easier

**[1:16:15]** to almost to do like role playing as opposed to being yourself you can actually like be the like really imagine yourself as the leader of France or Russia and so on like really pretend to be that person it's actually fun to really lean into being that that leader yeah so some some players do go this route where they just like kind of view it as a strategy game but also a role-playing game where they can like act out like what would I be like if I

**[1:16:38]** was you know a leader of France in 1900 a forfeit right away no I'm just kidding um and they sometimes use like the old-timey language to like um or how they imagine the elites would talk at that time anyway so the what are the different turns of the game like what are the rounds yeah so on on every turn you got like a bunch of different units that you start out with so you start out um controlling like just a few units and the object of the game is to

**[1:17:07]** gain control of a majority of the map if you able if you're able to do that then you've won the game but like I said the only way that you're able to do that is by working with other players so on every turn you can issue a move order so for each of your units you can move them to an adjacent territory or you can keep them where they are or you can support a move or a hold of a different units so what are the territories how how is the map divided

**[1:17:32]** up it's kind of like Risk where the the map is divided up into like 50 different territories um now you can enter a territory if you're moving into that territory with more supports than the person that's in there or the person that's trying to move in there so if you're moving in and there's somebody already there um then if neither of you have support it's a one versus one and you'll bounce back another if you'll make progress if

**[1:17:54]** you have a unit that's supporting that move into the territory then it's a two versus one and you'll kick them out and they'll have to retreat somewhere what does support mean support is like it's it's an action that you can issue in the game so you can say this unit you write down this unit is supporting this other unit into this territory are these units from opposing forces they could be they could be and this is this is where the

**[1:18:16]** interesting aspect of the game comes in because you can support your own units into territory but you can also support other people's units into territories and so that's what the negotiations really revolve around but you don't have to do the thing you say you're going to do and this yeah and so you can say I'm going to support you but then backstab the person yeah that's absolutely right and that tension is core to the game the

**[1:18:38]** attention is absolutely core to the game the the fact that you can make all sorts of promises but you have to reason about the fact that like hey they might not trust you if you say you're going to do something or they might be lying to you when they say they're going to support you so maybe just just to jump back what's what's the history of the game in general is it true that Henry Kissinger loved the game and JFK and all those

**[1:19:02]** I've heard like a bunch of different people that or is that just one of those things that the cool kids say they do but they don't actually play so the game was created in the 50s yeah um and from what I understand it was um JFK's it was played in like the JFK White House Henry Kissinger's favorite game I don't know if it's true but um that's definitely what I've heard it's interesting that they went with World War One

**[1:19:25]** when it was created after World War II so the story that I've heard for the creation of the game is it was created by um somebody that had looked at the history of the 20th century and they saw World War one as a failure of diplomacy so sure you know they saw the fact that this war broke out as like the the diplomats of all these countries like really failed to prevent a war and he wanted to create a game that would basically teach people about diplomacy

**[1:19:56]** um and it's really fascinating that like in his ideal version of the game of diplomacy nobody actually wins the game because the whole point is that if somebody is about to win then the other players should be able to work together to stop that person from winning and so the ideal version of the game is just one where nobody actually wins and you know it kind of has a nice like wholesome take-home message then that you know war war is ultimately futile

**[1:20:17]** and uh and that optimal

**[1:20:24]** that feudal optimal could be achieved through great diplomacy yeah so uh is

**[1:20:30]** there some asymmetry in in terms of which is more powerful Russia versus Germany versus France and so on so I think the general consensus is that France is the strongest power in the game but the beautiful thing about diplomacy is that it's it's self-balancing right so it's the fact that France has an inherent Advantage from the beginning means that the other players are less likely to work with it I saw that Russia has four

**[1:20:52]** units or four of something that the others have three of something that's true yeah so Russia starts off with four units while all the other players start with three but Russia is also in a much more vulnerable position because they have to like um they have a lot more neighbors as well got it larger territory more uh yeah right more border to defend okay uh

**[1:21:14]** what else is what else is important to know about the rules so there how many rounds are there like is this iterative game is there is it is it finite you just keep going indefinitely usually the game lasts uh I would say about 15 or 20 turns um there's in theory No Limit it could last longer but at some point I mean if you're playing a house game with friends at some point you just get tired and you all agree like okay we're gonna end the

**[1:21:37]** game here and call it a draw um if you're playing online there's usually like set limits on when the game will actually end and what's the end what's the termination condition like this this one country have to conquer

**[1:21:51]** everything else so if somebody is able to actually gain control of a majority of the map then then they've won the game and that is a solo Victory as it's called now that pretty rarely happens especially with strong players because like I said the game is designed to incentivize the other players to put a stop to that and all work together to stop the superpower um usually what ends up happening is that you know all the players agree to a

**[1:22:12]** draw and then the the score the the win is divided among the remaining players um there's a lot of different scoring systems the one that we used in our research um basically um gives a score relative to how much control you have of the map so the more that you control the higher you score what's the history of using this game as a benchmark for AI research do people use it yeah so people have been working on AI for diplomacy since about the 80s

**[1:22:41]** um there was some really exciting research back then but the approach that was taken was very different from what we see today I mean the research in the 80s was a very rule-based approach kind of kind of a heuristic approach it was very in line with the kind of research that was being done in the 80s you know basically trying to encode human knowledge into the strategy of the AI sure um and you know it's understandable I

**[1:23:04]** mean the game is so incredibly different and so so much more complicated than the kinds of games that people were working on like chess and go uh and poker that it was honestly even hard to like start getting making any progress in in diplomacy can you just formulate what is the problem from an AI perspective and why is it hard why is it a challenging game to solve so there's a lot of aspects in diplomacy that make it a huge

**[1:23:30]** challenge first of all you have the natural language components and I think this really is what makes it are really the most difficult game among like the major benchmarks the fact that you have to it's not about moving pieces on the board your action space is basically all the different sentences that you could communicate to somebody else in this game and um is there can we just like Linger on that so is part of it like the ambiguity in the

**[1:24:00]** language if it was like very strict if you narrowed the set of possible sentences you could do it would that simplify the game significantly the the real difficulty is the breadth of things that you can talk about um you can have natural language and other games and like Sellers of Catan for example like you could have a natural language Settlers of Catan AI but the things that you're going to talk about are basically like am I trading

**[1:24:26]** you two sheep for a wood or three sheep for a wood um whereas in a game like diplomacy the breadth of conversations that you're going to have are like you know am I going to support you are you going to support me in return which units are going to do what uh what did this other person say promise you uh they're lying because they told this other person that they're going to do this instead um if you help me out this turn then in

**[1:24:49]** the future I'll do these things that will help you out um the the depth and breadth of these conversations is is really complicated

**[1:25:00]** and it's all being done in natural language um now you could approach it and we actually consider doing this like you you know having a simplified language to make this complexity uh smaller But

**[1:25:13]** ultimately we thought the most impactful way of doing this research would be to address the natural language component head-on and just try to go for the full game up front just looking at sample games and what the conversations look like greetings England this should prove to be a fun game since all the private press is going to be made public at the end at the least it will be interesting to see if the Press changes because of that

**[1:25:37]** anyway good okay so there's like uh yeah that's just kind of like the generic readings at the beginning of the game I think that the meat comes a little bit later when you're starting to talk about like specific strategy and stuff I agree there are a lot of advantages to the two of us keeping in touch in our Nations makes strong natural allies in the middle game so that kind of stuff uh making friends making enemies yeah or

**[1:26:00]** like if you look at the next line so the person's saying like I've heard uh bits about a Lepanto and an octopus opening and basically telling Austria like hey just a heads up you know I've heard these whispers about like what might be going on behind your back yeah but so there's all kinds of complexities in that in the in the language of that right like to interpret what that what the heck that means it's hard for us humans

**[1:26:24]** but for yeah it's even harder because you have to understand like at every level the the semantics of that right I mean there's there's a complexity and understanding when somebody is saying this to me what does that mean and then there's also the complexity of like should I be telling this person this like I've overheard these these Whispers should I be telling this person that like hey you might be getting attacked by by this other power Okay so

**[1:26:49]** what how we're supposed to think about okay so that's the natural language how do you even begin trying to solve this game it seems like this seems like the touring test on steroids yeah and I mean there's there's the natural language aspect and then even besides the natural language aspect you also have the The Cooperative elements of the game and I think this is actually um something that I find really interesting if you look at all the

**[1:27:10]** previous game AI uh breakthroughs they've all happened in these purely adversarial games where you don't actually need to understand how humans play the game it's all just AI versus AI right like you look at uh Checkers chess go poker Starcraft Dota 2 like in some

**[1:27:30]** of those cases they leveraged human data but they never needed to they were always just trying to have a scalable algorithm that then they could throw a lot of computational resources out a lot of memory at and then eventually it would converge to an approximation of a Nash equilibrium this perfect strategy that in the two player zero some game guarantees that they're going to be able to not lose to any opponent so you can't leverage self-play

**[1:27:54]** to solve this game you you can leverage self-play but it's no longer sufficient to beat humans so how do you integrate the human into the loop of this so what you have to do is incorporate human data and to kind of give you some intuition for why this is the case like imagine you're playing a negotiation game like like diplomacy um but you're training completely from scratch without any human data the AI is not going to suddenly like figure out how to

**[1:28:21]** communicate in English it's going to figure out some weird robot language that only it will understand yeah and then when you stick that in a game with six other humans they're gonna think this person's talking gibberish and they're just going to Ally with each other and team up against the bot or not even team up against the ball but just not work with the bot and so in order to be able to play this game with humans it has to understand the human

**[1:28:43]** way of playing the game not this machine way of playing the game yeah yeah that's fascinating so right the the there's a

**[1:28:53]** nuanced thing to understand because the a chess playing program doesn't need to play like a human to beat a human exactly but here you have to play like a human in order to beat them or at least you have to understand how humans play the game so that you can understand how to work with them if they have certain expectations about what does it mean to be a good Ally what does it mean to have like a reciprocal relationship where

**[1:29:14]** we're working together you have to abide by those conventions and if you don't they're just going to work with somebody else instead do you think of this as a clean in some deep sense of the spirit of the touring test is formulated by Alan Turing is is it in some sense this is what the Turing test actually looks like so because of open-ended natural

**[1:29:39]** language conversation seems like

**[1:29:42]** very difficult to evaluate like here at a high stakes where humans are trying to win a game that seems like how you actually perform the Turing test I think it's different from the touring test like the way that the touring test is formulated it's about trying to distinguish a human from a machine and seeing Oh could the machine uh successfully pass as a human in this adversarial setting where the eight where the player is trying to

**[1:30:05]** figure out whether it's a machine or a human whereas in diplomacy it's not about trying to figure out whether this player is a human or a machine it's ultimately about whether I can work with this player regardless of whether they are a human or machine and can the machine do that better than a human can yeah I'm going to think about that but that just feels like the implied requirement for that is for

**[1:30:32]** the machine to be human-like I think that's I think that's true that if you're going to play in this human game you have to somehow adapt to the to the human surroundings and the human playstyle and to win you have to adapt so you can't if you're the outsider if you're not human-like I feel like that's a losing strategy I think that's I think that's correct yeah yeah so okay uh

**[1:30:59]** what what are the complexities here what was your approach to it before I get to that one thing I should explain like why we decided to work on diplomacy so basically what happened is in 2019

**[1:31:11]** um I was wrapping up the work on six player poker on pluribus and was trying to think about what to work on next and I had been seeing like all these other breakthroughs happening in AI I mean like 2019 you have Starcraft you have Alpha star beating humans and Starcraft you've got the Dota 2 stuff happening at open AI you have GPT 2 or GPD 3 coming I think it was gpd2 at the time and it became clear that AI was progressing

**[1:31:35]** really really rapidly and people were throwing out these like other games about you know what should be the next challenge for for multi-agent AI and I just felt like we had to aim bigger um if you look at a game like chess or a game like go they took decades for researchers to to ultimately reach superhuman performance at I mean like chess took 40 Years of AI research go took another 20 years um and we we thought that diplomacy would be

**[1:32:06]** this incredibly difficult challenge that could easily take a decade to make an AI that could play competently um but we felt like that was that was a goal worth aiming for um and so honestly I was kind of reluctant to work on it at first because I thought it was like too far out of the realm of possibility but you know I was talking to a co-worker of mine Adam Lear and he was basically saying like yeah why not aim for it you know we'll learn some

**[1:32:30]** interesting things along the way and maybe it'll be possible um and so so we decided to go for it and I think I think it was the right choice considering just how much progress there there was in Ai and that that progress has continued in the years since so winning in diplomacy what does that really look like it means talking to six

**[1:32:53]** other players six other entities agents

**[1:32:57]** and convincing and convincing them of stuff that you want them to be convinced of like what what exactly I'm trying to get like to deeply understand what the problem is ultimately the problem is it's simple to to quantify right like you're going to play this game with humans and you want your score on average to be um as high as possible you know if you can say like I am winning more than any any human alive um then you're a champion diplomacy

**[1:33:26]** player um now ultimately we haven't we didn't reach that we got to human level performance we actually so we played about 40 games with with real humans online uh the bot came in second out of all players that played five or more games and um so not like number one but way way higher than well what was the expertise level are the beginners are they intermediate players Advanced players so no sense that's a great question and so I think

**[1:33:53]** this kind of goes into how do you measure the performance in diplomacy and I would argue that when you're measuring performance in a game like this you don't actually want to measure it in games with all expert players uh it's kind of like if you're developing a self-driving car you don't want to measure that car on the road with a bunch of expert stunt drivers you want to put it on a road of like an actual American city and see is this car

**[1:34:15]** crashing less often than an expert driver would so so that's the metric that we've used we we're saying like we're going to stick this game we're gonna stick this bot in games with a wide variety of skill levels and then are we doing better than a strong or expert human player would in the same situation that's quite brilliant because I played a lot of sports in my life like as a tennis Judo whatever and it's it's somehow almost easier to

**[1:34:42]** go against experts almost always I don't I think they're more predictable in the quality of play the the space of strategies you're operating under is narrower against experts it's more fun it's really frustrating to go against beginners also because beginners talk trash to you when they somehow do beat you so that's a human thing that AI doesn't have to be worry about that but yeah the variants and strategies right is greater especially with natural

**[1:35:09]** language it's just all over the place then true yeah and honestly when you look at what makes a good human diplomacy player um obviously they're able to handle themselves in games with other expert humans but where they really shine is when they're playing with these weak players and they know how to take advantage of the fact that they're a weak player that they won't be able to like pull off a stab as well or that they have certain Tendencies and they

**[1:35:33]** can take them under their wing and persuade them to do things that might not even be in their interest um the really good diplomacy players are able to to take advantage of the fact that there is that there are some weak players in the game okay so if you have to incorporate human play data how do you do that how do you do that in order to train an AI system to play diplomacy yeah so that's that's really the Crux of the problem how do we

**[1:35:58]** um leverage the benefits of self-play that have been so successful in all these other previous games while keeping the strategy as uh as human compatible as possible and so what we did is we first trained a language model um and then we made that language model controllable on a set of in a set of intents what we call intense which are basically like an action that we want to play and an action that we would like the other player to play and so this

**[1:36:25]** gives us a way to generate dialogue that's not just trying to imitate the human style um whatever a human would say in the situation but to actually give it a a an intent of purpose in its communication we can talk about a specific move or we can make a specific request and the determination of what that move is that we're discussing comes from

**[1:36:48]** um strategic strategic reasoning model that uses reinforcement learning and planning so the Computing the intents

**[1:36:55]** for all the players how's that done just so as a starting point is that with reinforcement learning or is that just optimal determining what the optimal is for intents It's a combination of reinforcement learning and planning

**[1:37:11]** um actually very similar to how you approach how we approached poker and how people approached like chess and go as well we're using self-play and and search to try to figure out what are what is an optimal move for us and what is a desirable move that we would like this other player to play now the the difference between the way that we approached reinforcement learning and search in this game versus those previous games is that we have to keep

**[1:37:36]** it human compatible we have to understand how the other person is likely to play rather than just assuming that they're going to play like a machine and how language gets them to play

**[1:37:49]** um in a way that maximize the chance of following the intent you want them to follow okay how do you do that how do you how do you connect language to intent so the way that RL and and planning is done is actually not using language so we're coming up with this like plan for the action uh that we're gonna play and the other person's gonna play and then we feed that action into the dialogue model that will then send a message according to those plans so the

**[1:38:12]** language model there is mapping action to to message to message

**[1:38:21]** one word at a time uh basically one message at a time so we'll we'll feed into the dialogue model like here are the actions that you should be discussing here's the message here's like the the content of the message that we would like you to send and then it will actually generate a message that corresponds to that okay does this actually work it works surprisingly well okay how

**[1:38:43]** oh man the the number of ways it probably goes horribly I would have imagined it goes horribly wrong um so how the heck is it effective at all I mean there are a lot of ways that this could fail so for example I mean you could have a situation where you're you're basically like we don't tell the the language model like here are the pieces of our action or the other person's action that you should be communicating and so like

**[1:39:08]** let's say you're about to attack somebody you probably don't want to tell them that you're going to attack them but there's nothing in the language like the language model is not very smart at the end of the day so it doesn't really have a way of knowing like well what should I be talking about should I tell this person I'm about to attack them or not um so we have to like develop a lot of other techniques that that deal with

**[1:39:26]** that um like one of the things we do for example is we try to calculate if I'm going to send this message what would I expect the other person to do in response so if it's a message like hey I'm going to attack you this turn they're probably gonna you know attack us or or defend against that attack and so we have a way of recognizing like hey sending this message is a negative expected value action and we should not send this message

**[1:39:53]** so yes for particular kinds of messages you have like an extra function that does the uh estimates the value of that message yeah so we have these kinds of filters that like so it's a filter so there's a there's a good and is that filter in your network or is it rule based that's that's a that's a neural network so we're well it's a it's a combination it's a neural network but it's also using planning um it's trying to compute like what is

**[1:40:18]** the policy that the other players are going to play Given that this message um has been sent and then is that better than not sending the message or not I feel like that's how my brain works too like there's a language model that generates random crap and then there's these other neural Nets they're

**[1:40:37]** essentially filters at least that's when I tweet I'll usually my process of tweeting I'll think of something and it's hilarious to me and then about five seconds later the filter Network comes in and says no no that's not funny at all I mean there's some something interesting to that kind of process so you have a set of actions that you you want you have an intent that you want to achieve an intent that you want your opponent to achieve then

**[1:41:02]** you generate messages and then you evaluated those messages will achieve the the the uh the goal you want yeah and we're filtering for several things we're filtering like is this a sensible message you know so sometimes language models will send will generate messages that are just like totally nonsense um and we try to filter those out we also try to filter out messages that that are basically lies um so you know diplomacy has this

**[1:41:29]** reputation as a game that's really about um deception and lying but we try to actually minimize the amount that the bot would lie um this was actually mostly or are you no I'm just kidding okay I mean like part of the reason for this is that we actually found that lying would make the bot perform worse in the long run it would end up with a lower score because once the bot lies um people would never trust it again and and trust is a huge aspect of the

**[1:41:59]** game of diplomacy taking notes here because I think this is applies to to life lessons too oh I think it's a really yeah really strong so like lying is a dangerous thing to do like you you want to avoid obvious lying yeah I mean I think when people play diplomacy for the first time they approach it as a game of deception and lying and and they ultimately if you talk to top diplomacy players what they'll tell you is that

**[1:42:24]** diplomacy is a game about trust and being able to build trust in an environment that encourages people to not trust anyone so so that's the ultimate tension in diplomacy how can this AI reason about whether you are being honest in your communication and how can the AI persuade you that it is being honest when it is telling you that hey I'm actually going to support you this turn is there some sense I don't know if you

**[1:42:48]** step back and think that this process well indirectly help us study human psychology so like if trust is the ultimate goal wouldn't that help us understand what are the fundamental aspects of forming trust between humans and between humans and AI I mean that's a really really important question that's much bigger than the strategy games it's how can that that's fundamental to the human robot interaction problem how do we form

**[1:43:17]** Trust between intelligent entities so one of the things I'm really excited about with diplomacy um there's never really been a good domain to investigate these kinds of questions yeah um and diplomacy gives us a domain where trust is really at the center of it um and it's not just like you've hired a bunch of mechanical turkers that you know are being paid and trying to get through the task as quickly as possible you have these people that are really

**[1:43:46]** invested in the outcome of the game and they're really trying to do the best that they can um and so I'm really excited that we're able to we actually like have put together this we're open sourcing all of our models we're open sourcing uh all of the all the code and we're making the data that we've used available to researchers um so that they can investigate these kinds of questions so the data of the different the human and the AI play of

**[1:44:11]** diplomacy and the models that you use for the generation of the messages and the filtering yeah not not just even the data of the AI playing with the humans but all the training data that we that we had that we used to train the AI to understand how humans play the game we're setting up a system where researchers will be able to apply um to be able to gain access to that data and be be able to to use it in their own research we should say what is

**[1:44:37]** the name of the system we're calling the bot Cicero Cicero and what's the name like you're open sourcing what's the name of the repository and and the like the the project is it also just called Cicero the big project or are you still coming up with the name the the data set comes from this website web diplomacy.net is this site that's been online for like 20 years now and uh it's one of the main sites that people use to play diplomacy

**[1:45:00]** on it we've got like 50 000 games of diplomacy with you know natural language communication um over 10 million messages so it's a pretty massive data set that people can use to um we're hoping that the the academic Community the research Community is able to use it for for all sorts of interesting research questions so do you from having studied this game is this a sufficiently rich problem space to explore this kind of human AI

**[1:45:28]** interaction yeah absolutely and I think it's I think it's maybe the best data set that I can think of out there to to investigate these kinds of questions of um negotiation trust um persuasion I wouldn't say it's the best data set in the world for um human AI interaction that's a very broad field but I think that it's definitely up there is like you know if you're really interested in language models interacting with humans in you

**[1:45:54]** know a setting where their incentives are not fully aligned this seems like an ideal data set for investigating that so you have um you have a paper with some impressive results and just an impressive paper they're taking this problem on what's the most exciting thing to you in terms of the results from the the paper

**[1:46:17]** well I think there's ideas or results yeah I think there's a few aspects of the results and um that I think are really exciting so first of all the fact that we were able to achieve such strong performance um I was surprised by and pleasantly surprised by um so we played 40 games of diplomacy with real humans and the bot placed second out of all players that have played five or more games so it's about 80 players total

**[1:46:42]** um 19 of whom played five or more games and the bot was ranked second out of those players um and the bot was was really good in two Dimensions one being able to establish strong connections with the other players on the board being able to like persuade them to work with it um being able to coordinate with them about like how it's going to work with them and then also the Raw tactical and strategic aspects of the game you know being able to understand

**[1:47:09]** what the other players are likely to do being able to model their behavior and respond appropriately to that the bot also really excelled at what are some interesting things that the bot said by the way are you allowed to swear in the um okay are there rules to what you're allowed to say and not in diplomacy you can say whatever you want I think the site will get very angry at you if you start like threatening somebody and if we actually like if

**[1:47:33]** you're threaten somebody you're supposed to do it politely yeah politely you know keep it in character um we actually had a researcher watching the bot 24 7 for well whenever we play a game we had a bot watching it to make sure that it wouldn't go off the rails and start like threatening somebody or something like that I would just love it if the boss started like mocking mocking everybody like some weird quirky strategies would emerge have you seen

**[1:47:58]** anything interesting that you huh that's a weird that's a that's a behavior either of the filter or the language model that was weird to you that was yeah they were definitely like things that the bot would would do that were not in line with like how humans would approach the game and that in a good way the humans actually you know we we've talked to some expert diplomacy players about these results and their takeaways that

**[1:48:24]** well maybe humans are approaching this the wrong way and this is actually like the right way to play the game um so what's required to win like what

**[1:48:36]** um what does it mean to mess up or to exploit the sub-optimal behavior of a player like uh is there is there optimally rational behavior and irrational behavior that you need to estimate that kind of stuff like what what stands out to you like is there a crack that you can exploit is there like um a weakness that you can exploit in the game that that everybody's looking for well I I think you're asking kind of two questions

**[1:49:03]** there so one like modeling the irrationality and the suboptimality of humans um you can't in diplomacy you can't treat all the other players like they're machines and if you do that you're you're going to end up playing really poorly and so we actually ran this experiment so we we trained a bot in a two-player zero-sum version of diplomacy um the same way that you might approach a game like chess or poker and the bot was superhuman it would crush any

**[1:49:30]** competitor and then we took that same training approach and we trained a bot for the full Seven Player version of the game through self-play without any human data and we stuck it in a game with six humans and it got destroyed even in the version of the game where there's no explicit natural language communication it still got destroyed because it just wouldn't be able to understand how the other players were approaching the game

**[1:49:51]** and be able to to work with that can you just Linger on that meeting like there's an individual there's an individual personality each player and then you're supposed to remember that but Woody means it's not able to understand the the players well it would

**[1:50:07]** for example expect the human to support it in a certain way when the human men would simply like think like no I'm not supposed to support you here um it's kind of like you know if you develop a self-driving car and it's trained completely from scratch with other self-driving cars it might learn to drive on the left side of the road that's a totally reasonable thing to do if you're with these other self-driving cars that are also driving on the left

**[1:50:28]** side of the road but if you put it in an American city it's gonna crash but I guess the intuition I'm trying to build up is why does it then crush a human play on heads up this is multiple this is an aspect of two player zero song versus games that involve cooperation so in a two-player zero-sum game um you can do self-play from scratch and you will arrive at the Nash equilibrium where you don't have to worry about the

**[1:50:52]** other player playing in a very human sub-optimal style that's just going to be that the only way that deviating from an ash equilibrium

**[1:51:04]** would would change things is if it helped you so I what's the dynamic of cooperation that's effective in diplomacy do you always have to to have one friend in the game you always want to maximize

**[1:51:17]** your friends and minimize your enemies

**[1:51:22]** got it and

**[1:51:25]** boy in the the lying comes into play there so the more friends you have the better yeah I mean I guess you have to attack somebody or else you're not going to make progress all right so that's the tension but man this is too real this is too real to this is too too close to geopolitics of actual military conflict in the world okay uh that's fascinating so that cooperation element is what makes the game really really hard yeah and to give

**[1:51:50]** you an example of of how this sub-optimality and irrationality comes into play there's a really common situation in a game of diplomacy um that where one player starts to win and they're like at the point where they're controlling about half the map yeah um and the remaining players who have all been fighting each other the whole game all have to like work together now to stop this other player from winning or else everybody's gonna

**[1:52:13]** lose um and it's kind of like you know Game of Thrones like I don't know if you've seen the show like you know you got the the others coming from the north and like all the people have to start work out their differences and stop them from from taking over um and the bot will do this like the bot will work with the other players to stop the superpower from winning but if it doesn't really if it's trained from scratch or it doesn't really have a good

**[1:52:36]** grounding in how humans approach it it will also at the same time attack the other players with its extra units so all the units that are not necessary to stop the superpower from winning it will use those to grab as many centers as possible from the other players and in totally rational play the other players should just live with that you know they have to understand like hey a score of one is better than a score of

**[1:52:58]** zero so um so okay he's grabbed my centers but I I'll just deal with it but humans don't act that way right the human gets really angry at the bot and ends up throwing the game because you know I'm gonna screw you over because you did something that's not fair to me got it and are you supposed to model that is the boss supposed to model that kind of human frustration yeah exactly

**[1:53:25]** and so that is something that seems almost impossible to model purely from scratch without any human data it's a very cultural thing yeah um and so you need human data to be able to understand that hey that's how humans behave and you have to work around that it might be suboptimal it might be rational but but that's an aspect of humanity that you have to have you have to deal with so how difficult is it to train on human

**[1:53:47]** data given that human data is very limited versus what the US a purely self-play mechanism can generate that's actually one of the major challenges that we faced in the research that we had a good amount of human data we had about 50 000 games what we try to do is leverage as much soft play as possible while still leveraging the human data so

**[1:54:09]** what we do is we do self-play very similar to how it's been done in poker and go but we try to regularize the self-play towards the human data basically the way to think about it is

**[1:54:22]** um we penalize the bot for choosing

**[1:54:27]** actions that are very unlikely under how under the human data set and how do you know is there is this some kind of function that says this is human-like enough yeah so we we train a bot through supervised learning to model the human play as much as possible so we basically like train a neural net um on those 50 000 games and that gives us an approximate that gives us a policy that resembles to some extent how humans actually play the game now this isn't a

**[1:54:53]** perfect model of human play because we don't have unlimited data we don't have unlimited neural net capacity um but it gives us some approximation uh is there some data on the internet that's useful besides just diplomacy so on the language side of things is there some can you go to like Reddit and

**[1:55:14]** um so sort of background model formulation that that's useful for the game of diplomacy yeah absolutely and so for the language model which um it's kind of like a separate question you know we didn't use the language model during self-play training but we

**[1:55:27]** pre-trained the language model on you know tons of internet data as much as possible and then we fine-tuned it specifically on the diplomacy games so we are able to like Leverage The Wider data set in order to fill in some of the gaps in like how communication happens more broadly besides just like specifically in these diplomacy games Okay cool so what what's some what are some interesting things that came to life from this from this

**[1:55:49]** work uh to you like what are some insights about

**[1:55:57]** um about games where natural language is involved and cooperation deep cooperation is involved well I think there's a few insights um so first of all the fact that you can't rely purely or

**[1:56:11]** even largely on self-play that you really have to have an understanding of how humans approach the game um I think that that's one of the major conclusions that I'm drawing from this work um and that is I think applicable more broadly to a lot of different games so we've actually already taken the approaches that we've used in diplomacy and tried them on uh Cooperative card game called Hanabi and we've had a lot of success in that game as well

**[1:56:33]** um on the language side I think the fact that we were able to control the language model through this

**[1:56:43]** intense approach was very effective

**[1:56:47]** um and it allowed us instead of just imitating how humans would communicate were able to go beyond that and able to feed into it superhuman strategies that

**[1:56:58]** it can then um you know generate messages corresponding to is there something you could say about detecting whether a person or AI is lying or not the bot doesn't explicitly try to

**[1:57:12]** calculate whether somebody is lying or not but what it will do is try to predict what actions they're going to take given the communications given the messages that they've sent to us so given our conversation what do I think you're going to do and implicitly there is a calculation about whether you're lying to me in that you know if if you're based on your messages if I think you're going to attack me this turn um even though your messages say that

**[1:57:36]** you're not then you know essentially the bot is predicting that you're lying but it doesn't view it as as lying the same way that we would view it as lying but you could probably reformulate with all the same data and make a classifier lying or not yeah I think I think you could do that um that was not something that we were focused on but I think that it is possible that you know if you came up with some measurements of like what

**[1:58:02]** does it mean to tell a lie because there's there's a spectrum right like if you're withholding some information is that a lie um if you're mostly telling the truth but you forgot to mention this like one action out of like 10 is that a lie um it's hard to draw the line but you know if you're willing to do that and then you could possibly use it to uh dude this feels like an argument inside a relationship now what constitutes a

**[1:58:24]** lie um depends what you mean by the definition of the word is okay um still it's fascinating because trust and lying is all intermixed into this and it's language models that are becoming more and more sophisticated it's just a fascinating space to explore um what do you see as the future of this

**[1:58:51]** work um that is inspired by the Breakthrough performance that you're getting here with diplomacy

**[1:59:00]** uh I think there's a few different directions to take this work um I I think really what it's showing us is the potential that language models have I mean I think a lot of people didn't think that this kind of result was possible even today despite all the progress that's been made in language models and so it shows us how we can Leverage The Power of things like self-play on top of language models to get um increasingly better performance and

**[1:59:25]** the ceiling is really much higher than what we have right now is this transferable somehow to

**[1:59:35]** to chat Bots for the more General task of dialogue so because there is a kind of negotiation here a dance between entities that are trying to cooperate and at the same time a little bit adversarial which I think Maps somewhat

**[1:59:52]** to the general you know the entire process of Reddit or

**[1:59:58]** like internet communication you're cooperating you're adversarial you're having debates you're having uh camaraderie all that kind of stuff I think one of the things that's really useful about diplomacy is that we have a well-defined value function there is a well-defined score that the bot is trying to optimize and and in a in a setting like a general chatbot setting it needs it would need that kind of um objective in order to fully leverage

**[2:00:23]** the techniques that we've developed what about like what we talked about earlier with NPCs inside video games like how can it be used to create for Elder Scrolls 6 more compelling um

**[2:00:40]** NPCs that you could talk to instead of instead of committing all kinds of violence with a sword and fighting dragons just sitting in a Tavern and drink all day and talk to the chatbot the way that we've approached AI diplomacy is you condition the language on an intent now that intent and diplomacy is an is an action but it doesn't have to be and you can imagine you know you could have NPCs in video games or the metaverse or whatever where

**[2:01:04]** there's some intent or there's some objective that they're trying to maximize and you can specify what that is um and and then the language can correspond to that intent now I'm not saying that this is you know happening imminently but um I'm saying that this is like a future application potentially of this direction of research so what's the more General formulation of this making self-play be able to scale the way self-play does and still maintain

**[2:01:30]** human-like Behavior the way that we've approached self-play in diplomacy is like we're we're trying to come up with good intents to condition the language model on and the space of intents is actions that can be played in the game now there is like the potential to have a broader set of intents things like you know long-term cooperation or long-term uh objectives or you know

**[2:01:58]** gossip about what another player was saying um these are things that we're currently not conditioning the language model on and so it's not able to we're not able to control it to say like oh you should be talking about this thing right now but it's quite possible that you could expand the scope of intents to be able to allow it to talk about those things now in the process of doing that the self-play would become much more

**[2:02:18]** complicated um and so that is a potential for for future work okay the increasing the number of intents I still am not quite clear how you keep the self-play

**[2:02:32]** integrated into the human world yeah I'm a little bit loose on the uh uh on understanding how you do that so we train a neural Nets to um imitate the human data as closely as possible and that's what we call the anchor policy and now when we're doing self-play the the problem with the anchor policy is that it's not a perfect approximation of how humans actually play because we don't have infinite data because we don't have unlimited neural network

**[2:02:57]** capacity it's actually a relatively sub-optimal approximation of how humans actually play and we can improve that approximation by adding planning and RL

**[2:03:10]** and so what we do is we get a better approximation a better model of human play by during the self-play process we say you

**[2:03:20]** can deviate from this human anchor policy if there is an action that has you know particularly High expected value um but it would have to be a really high expected value in order to to deviate from from this human-like policy so you basically say try to maximize your expected value while at the same time stay as close as possible to the human policy and there is a parameter that controls those the the relative weighting of those Computing objectives

**[2:03:48]** so the question I have is how sophisticated can the anchor policy get to have a policy that approximates human behavior right yeah so as you increase

**[2:04:02]** the number of intents as you generalize the the space in which this is applicable and given that the human data is limited try to anticipate a policy that works for in a much larger number of cases like how how difficult is the process of forming a damn good anchor policy well it really comes down to how much human data you have so it's all boss scale in the human data I think the more human data you have the better and I

**[2:04:28]** think that that's going to be the major bottleneck in in scaling to to more complicated um domains but that said you know there might be the potential just like in the language model where we leveraged you know tons of data on the internet and then specialized it for diplomacy um there is the future potential that you can leverage huge amounts of data across the board and then specialize it in the data set that you have for

**[2:04:52]** diplomacy and in that way you're essentially augmenting the amount of data that you have to what degree does this apply to the general the real world diplomacy

**[2:05:06]** the geopolitics you know there's a game theory has a history of being applied to understand and to give us hope about nuclear weapons for example the mutually assured destruction is a game theoretic concept that you can formulate some people say it's oversimplified but nevertheless here we are and we somehow haven't blown ourselves up do you see a future where this kind of this kind of system can be used to help us make decisions geopolitical decisions

**[2:05:34]** in the world well like I said the original motivation for the game of diplomacy was the failures of World War One The Diplomatic failures that led to War uh and the real take-home message of diplomacy is that you know if people approach diplomacy the right way then war is ultimately unsuccessful

**[2:05:58]** um the way that I see at war is an inherently negative sum game right there's always a better outcome than War for all the parties involved and my hope is that you know as AI progresses then maybe this technology could be used to help people make better decisions um across the board and you know hopefully avoid negative some outcomes like War yeah I mean I just came back from Ukraine I'm going back there on deep

**[2:06:27]** personal levels think a lot about

**[2:06:32]** how peace can be achieved and I'm a big believer in conversation or leaders getting together and having conversations and trying to understand each other yeah it's fascinating to think um whether each one of those leaders can run a simulation ahead of time like if I'm an

**[2:06:51]** what are the possible consequences if I'm nice what are the possible consequences um my guess is that if the president of the United States got together with uh Vladimir zielinski and Vladimir Putin that there will be significant benefits

**[2:07:09]** to um the president United States not having an ego of kind of playing down of giving away a lot of chips for the future successful world so

**[2:07:22]** giving a lot of power to the two presidents of the competing Nations to achieve peace that's my guess but it'd be nice to run a bunch of simulations but then you have to have human data right you really because it's like the game of diplomacy is fundamentally different than geopolitics you need data you need like I guess that's the question I have like how transferable is this to uh like I don't know any kind of negotiation right like to any kind of

**[2:07:46]** look some local I don't know a bunch of lawyers like arguing like at a divorce like divorce lawyers like how transferable this all kinds of human negotiation well I feel like this isn't a question that's unique to diplomacy I mean I think you look at RL breakthroughs reinforcement learning breakthroughs in previous games as well like you know AI for Starcraft AI for Atari you haven't really seen it deployed in the real world because you

**[2:08:10]** have these problems of it's really hard to collect a lot of data um and you don't have a you don't have a well-defined action space you don't have a well-defined reward function these are all things that you really need for reinforcement learning and planning to be really successful today now there are some domains where you do have that um code generation is one example theorem proving mathematics that's another example where you have a

**[2:08:36]** well-defined action space you have a well-defined reward function and those are the kinds of domains where I can see RL in the short term being incredibly powerful but

**[2:08:49]** yeah I think that those are the barriers to deploying this at scale in the real world but and the hope is that in the long run we'll be able to get there yeah but you see diplomacy feels like closer to the real world than does Starcraft like because it's natural language right you're operating in a space of intense and in a space of natural language that feels very close to the real world and it also feels like you could get data on

**[2:09:09]** that from the internet yeah and that's why I do think that diplomacy is taking a big step closer to the real world than anything that's came before in terms of game AI breakthroughs the fact that you know we're we're communicating in natural language we've we're leveraging the fact that we have this like General data set of uh dialogue and communication from a breadth of the internet um that is that is a big step in that

**[2:09:37]** direction we're not 100 there but um but we're getting closer at least so if we actually return back to Poker and chess are some of the ideas that you're learning here with diplomacy could you construct AI systems that play like humans like um make for a fun opponent

**[2:09:58]** in a game with Jess yeah absolutely we've already started looking into this direction a bit so we tried to use the techniques that we've developed for diplomacy uh to make chess and go AIS and what we found is that it led to much more human-like strong chess and go players the way that

**[2:10:17]** AIS like stockfish today play is in a very inhuman style it's very strong but it's very different from how humans play and so we can take the techniques that we've developed for diplomacy we do something similar in um in chess and go and we end up with the bot that's both strong and human-like

**[2:10:37]** um to elaborate on this a bit like one way to approach making a human-like AI for chess is to collect a bunch of human games like a bunch of human Grand Master games and just do supervised learning on those games but the problem is that if you do that what you end up with is an AI That's substantially weaker than the human Grand Masters that you've trained on because the neural net is not able to approximate the the Nuance of the

**[2:11:02]** strategy this goes back to the planning thing that I mentioned the search thing that I talked about before that these human Grand Masters when they're playing they're using search and they're using planning and the neural net alone unless you have a massive neural net that's like a thousand times bigger than what we have right now it's not able to approximate those details very effectively and on the other hand you can leverage

**[2:11:26]** search and planning very heavily but then what you end up with is an AI that plays in a very different style from how humans play the game now if you strike this intermediate balance by setting the um the regularization parameters correctly and say you can do planning but try to keep it close to the human policy then you end up with an AI that plays in both a very human-like style and a very strong style and you can actually even tune it

**[2:11:52]** to have a certain ELO rating so you can say play in the style of like a 2800 elohuman um I wonder if you could do specific type of humans or categories of humans so not just skill but Style yeah I think so and so this is this is where the the research gets interesting like you know one of the things that I was thinking about is and this is actually already being done I think there's a researcher at the University of Toronto that's working on this

**[2:12:19]** um is to make an ad that plays in the style of a particular player like Magnus Carlson for example you can make an AI that plays like Magnus Carlson and then where I think this gets interesting is like maybe you're up against Magnus Carlson in the world championship or something you can play against this Magnus Carlson bot to prepare against the real Magnus Carlson and you can try to explore strategies that he might struggle with

**[2:12:43]** um and try to figure out like how do you beat this player in particular um on the other hand you can also have Magnus Carlson working with this bot to try to figure out where he's weak um and where he needs to improve his strategy um and so I can Envision this future where data on specific chess and go

**[2:13:03]** players becomes extremely valuable because you can use that data to create specific models of how these particular players play so increasingly human-like behavior and Bots however as you've mentioned makes cheating cheat

**[2:13:17]** detection much harder it it does yeah the way that sheet detection Works in a game like poker and a game like chess and go from what I understand is trying to see like is this person making moves that are very common among chess AIS or

**[2:13:34]** you know AIS in general um but very uncommon among top human players and if you have the development of these AIS that play in a very strong style but also a very human-like style then that poses serious challenges for cheat detection and it makes you now ask yourself a hard question about what is the role of AI systems as they become more and more integrated in our society and this kind of human AI

**[2:14:03]** um integration has has some deep ethical

**[2:14:07]** issues that we should be aware of and also it's a kind of cyber security challenge right for to make you know one of the assumptions we have when we play games is that there's a trust that is only humans involved and there

**[2:14:22]** the better AI systems to create which makes it super exciting human-like AI systems with different styles of humans is really exciting but then we have to have the defenses better and better and better if we're to trust that we uh can enjoy human versus human game in a deeply Fair way it's fascinating so it's just uh it's humbling yeah I think there is a lot of like negative potential for this kind of Technology but you know at

**[2:14:47]** the same time there's a lot of upside for it as well so you know for example right now it's really hard to learn how to get better in games like chess and poker and go because the way that the AI plays is so foreign and incomprehensible but if you have these AIS that are playing you know you can say like Oh I'm a 2000 ELO human how do I get to 2200 now you can have an AI that plays in the style of a 2200 elohiman and that will

**[2:15:10]** help you get better or you know you mentioned this problem of like how do you know that you're actually playing with humans when you're playing like online in video games well now we have the potential of populating these like Virtual Worlds with um agents like AI agents that are actually fun to play with and you don't have to always be playing with other humans to to you know have a fun time so yeah a lot a lot of upside potential

**[2:15:36]** too and I think you know with any sort of tool there's there's the potential for a lot of greatness and a lot of uh downsides as well so in the paper they got a chance to look at there's a section on uh ethical considerations what's in that section what are some ethical considerations here is it some of the stuff we've already talked about there's some things that we've already talked about um I think specific to diplomacy you know there's

**[2:15:58]** there's also the the challenge that the game is you know there is a deception aspect to the game um and so you know have developing language models that are capable of deception is I think a dicey issue and something that you know makes research on diplomacy particularly challenging um and you know so so those kinds of issues of like should we even be developing AIS that are capable of lying to people that's something that we have to you

**[2:16:27]** know think carefully about uh that's so cool I mean that you have to do that kind of stuff in order to figure out where the ethical lines are but I can see in the future it being illegal to have a consumer product that

**[2:16:40]** lies yeah yeah like your personal assistant AI system is not a lot is always have to tell the truth but if if I ask it do I do I look did I get fatter over the past month I sure as hell want that AI system to lie to me uh so there's a trade-off between lying and being and being nice after somehow find

**[2:17:03]** where's the ethics in that and we're back to discussions inside relationships anyway what were you saying oh yeah I was getting like yeah this yeah that's kind of going to the question of like what what is a lot you know is a white lie a bad lie is it an ethical lie yeah you know those kinds of questions uh boy we return time and time again to deep human questions as we design AI systems that's exactly what they do they put a

**[2:17:23]** mirror to humanity to help us understand ourselves there's there's also the issue of like you know in these diplomacy experiments in order to do a fair comparison you know what we found is that there's an inherent anti-ai bias in these kinds of games so we actually played a tournament in a non-language version of the game where you know we we told the participants like hey in every single game there's going to be an AI

**[2:17:47]** and what we found is that the humans would spend basically the entire game like trying to figure out who the bot was and then as soon as they thought they figured it out they would all team up and try to kill it um and you know overcoming that inherent

**[2:18:02]** anti-ai bias is is a challenge um on the flip side I think when robots become the enemy

**[2:18:11]** that's when we get to heal our human divisions and then we can become one as long as we have one enemy it's it's that Reagan thing when aliens show up that's when we we put our side our divisions we've become one one human species right you might have our differences but we're at least all human at least we all hate the robots no no no I think there will be actually in the future something like a civil rights movement for robots I

**[2:18:33]** think that's the fascinating things about AI systems and is they ask they force us to ask about ethical questions about what is sentience what is uh how do we feel about systems that are capable of suffering or capable of displaying suffering and how do we design products that show emotion and not how do we feel about that lying is another topic are we going to allow Bots to lie and not and where's the balance between being nice

**[2:19:00]** and and telling the truth I mean these are all fascinating human questions it's like so exciting to be in the century when we create systems that

**[2:19:12]** take these philosophical questions that have been asked for centuries and now we can engineer them inside systems where like you really have to answer them because you'll have transformational impact on human society depending on what you design inside those systems it's fascinating and like you said I feel like diplomacy is a step towards the direction of the real world applying these RL methods towards the real world

**[2:19:37]** from from all the Breakthrough performances and go and chess and Starcraft and DOTA this is this feels like the real world especially now my mind's been on war in military conflict this feels like it can give us some deep insights about human behavior at the large geopolitical scale

**[2:19:57]** um what do you think is the um breakthrough

**[2:20:04]** or the directions of work that will take us towards solving intelligence towards creating AGI systems you've been a part of creating

**[2:20:16]** um by the way we should say a part of great teams that do this of creating

**[2:20:22]** systems that achieve breakthrough performances on before thought unsolvable problems like poker uh

**[2:20:30]** multiplayer poker diplomacy

**[2:20:33]** we're taking steps towards that direction what do you think it takes to go all the way to create superhuman level intelligence you know there's a lot of people trying to figure that out right now um and you know I should say like the amount of progress that's been made especially in the past few years is truly phenomenal I mean you look at where AI was 10 years ago and the idea that you could have AIS that can generate language and generate images

**[2:20:54]** the way they're doing today and able to play a game like diplomacy was just like Unthinkable um even even five years ago let alone ten years ago um now there are there are aspects of AI that I think are still lacking um I think there's General agreements that

**[2:21:15]** one of the major issues with AI today is that it's very data inefficient it's very it requires a huge number of samples of training examples to be able to train you know you look at an AI that plays go and it needs millions of games of go to uh to learn how to play the game well whereas a human can pick it up in like you know I don't know how many games does a human go player go go Grand Master play in their lifetime probably

**[2:21:37]** you know in the thousands or tens of thousands I guess um so that's that's one issue overcome efficiency overcoming this challenge of data efficiency and this is particularly important if we want to deploy AI systems in real world settings

**[2:21:55]** um where they're interacting with humans because you know for example with robotics it's really hard to generate a huge number of samples it's it's a different story when you're working in these you know totally virtual games where you can play a million games and it's no big deal I was planning on just launching like a thousand of these robots in Austin I don't think it's illegal for Lego robots to roam the streets and just collect data that's not

**[2:22:15]** of course the worst that could happen yeah I kind of I mean that's one way to overcome the data efficiency problem is like scale it yeah like I actually tried to see if there's a law against robots like Lego robots just operating

**[2:22:30]** in in this in the streets of a major city and there isn't I couldn't find any so um I'll take it all the way to the Supreme Court robot rights okay anyway sorry you were saying so the so what what are the ideas for getting becoming more data efficient uh I mean that's that's the trillion dollar question in AI today I mean if you can figure out how to make AI systems more more data efficient then that's a huge breakthrough so nobody really

**[2:22:56]** knows right now it could be just a gigantic background model language model and then you do um the training becomes like prompting that model to uh to essentially do a kind of querying a search into the space of the things it's learned to customize that to whatever problem you're trying to solve so maybe if you form a large enough language model you can go quite quite a long way that you know I think there's some truth

**[2:23:21]** to that I mean you look at the way humans approach um a game like poker they're not coming at it from scratch they're coming at it with a huge amount of background knowledge about you know how humans work how the world Works um the idea of money so they're able to leverage that kind of information to uh to to pick up the game faster uh so it's not really a fair comparison to then compare it to an AI That's like learning

**[2:23:46]** from scratch and maybe one of the ways that we address this uh sample complexity problem is by allowing AIS to leverage that general knowledge across a ton of different domains so like I said you did uh a lot of incredible work in the space of research and actually Building Systems what advice would you give to uh let's start with beginners what advice would you give to beginners interested in machine learning just there at the very start of

**[2:24:10]** their Journey they're in high school and college thinking like this seems like a fascinating world what advice would you give them um I I would say that there are a lot of people working on similar aspects of machine learning and to not be afraid to try something a bit different my own path in AI is pretty atypical for a machine learning researcher today I mean I started out working on Game Theory and um and then shifting more towards

**[2:24:40]** reinforcement learning as time went on and that actually had a lot of benefits I think because it allowed me to look at these problems in a very different way from the way a lot of machine learning researchers view it and that comes with

**[2:24:57]** um drawbacks in some respects like I think there's definitely aspects of machine learning where you know I'm weaker than most of the researchers out there but I think that diversity of perspective um you know when I'm working with my teammates um there's something that I'm bringing to the table and there's something that they're bringing to the table and that kind of collaboration becomes very fruitful for that reason so there could

**[2:25:14]** be problems like like poker like you've

**[2:25:20]** chosen diplomacy that could be problems like that still out there that you can just tackle even if it seems extremely difficult

**[2:25:28]** um I think that there's a lot of challenges challenges left and I think having a diversity of viewpoints and

**[2:25:35]** backgrounds is really helpful for working together to figure out how to tackle those kinds of challenges so as a beginner so that I would say that's that's more for like a grad student they already built up a base like a complete beginner what's a good journey so for you that was doing some more on the math side of things doing Game Theory all that good so it's basically build up a foundation in something so programming

**[2:25:56]** mathematics it could even be physics but build build that Foundation yeah I would say build a strong foundation in math and computer science and statistics in these kinds of areas but but don't be afraid to try something that's different and learn something that's different from you know the the thing that everybody else is doing to get into machine learning um you know there's there's value in having a different background than everybody else

**[2:26:20]** um yeah so but certainly having a strong math background especially in things like linear algebra and statistics and probability um are incredibly helpful today for for learning about and understanding machine learning do you think one day we'll be able to since you're taking steps from poker to diplomacy one day we'll be able to uh

**[2:26:43]** figure out how to live life optimally well what is it like in in poker and diplomacy you need a value function you need to have a reward system and so what does it mean to live a life that's optimal so okay so then you can exactly

**[2:26:58]** like lay down a reward function being like I want to be rich or I want to be um I want to be in a happy relationship and then you'll say well do X you know there's there's a lot of uh talk today about in in AI safety circles about like this specification of you know reward functions so you you say like okay my objective is to be rich and maybe the AI tells you like okay well if you want to maximize the probability that you're rich go rob a bank sure and

**[2:27:25]** so you wanna is that is that really what you want is your objective really to be rich at all costs or is it more nuanced than that so the understand the consequences yeah

**[2:27:39]** yeah so yeah that that's so maybe life

**[2:27:44]** is more about defining the reward function that minimizes the unintended consequences than it is about the actual policy that gets you to the rewards function maybe life is just about constantly updating the reward function I think one of the challenges in life is is figuring out exactly what that reward function is sometimes it's pretty hard to specify the same way that you know trying to handcraft the optimal policy

**[2:28:07]** in a game like chess is really difficult it's not so clear-cut what the reward function is for for life I think one day AI will figure it out

**[2:28:20]** and I wonder what that would be until then I just really appreciate the kind of work you're doing and um it's it's really fascinating taking a leap into a more and more real world like

**[2:28:33]** um problem space and just achieving incredible results by applying

**[2:28:39]** reinforcement learning no since I saw you work on poker you've been in constant inspiration it's an honor to get to finally talk to you and uh this is really fun thanks for having me thanks for listening to this conversation with no Brown to support this podcast please check out our sponsors in the description and now let me leave you with some words from Sun Tzu and the Art of War the whole secret lies in confusing the

**[2:29:01]** enemy so that he cannot fathom our real intent thank you for listening and hope to see you next time

