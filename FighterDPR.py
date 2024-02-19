import random as rand 
from matplotlib import pyplot as plt
import statistics as stat

print("Program running... ")

class Character(object): 
    def __init__(self, num_smite): 
        self.damage = 0 
        self.crits = 0 
        self.crit = 1
        self.hit = 0
        self.hit_total = 0 
        self.advantage = 0 
        self.to_hit = [0,0]
        self.hits = [] 

        self.num_smite = num_smite 
        self.temp_smite = num_smite

    # Adds damage dice to an attack 
    def smite_dice(self, num, die): 
        if self.hit == 1 and self.temp_smite > 0: 
            for i in range(num * self.crit): 
                self.damage += rand.randint(1,die) 
            self.temp_smite -= 1

    # Adds a flat bonus to an attack 
    def smite_flat(self, add): 
        if self.hit == 1 and self.temp_smite > 0: 
            self.damage += add 
            self.temp_smite -= 1

    # Rolls a d20, includes parts for advantage
    def roll20(self, bonus): 
        if self.advantage == 2: 
            roll = max(rand.randint(1,20),rand.randint(1,20),rand.randint(1,20))
        elif self.advantage == 1:
            roll = max(rand.randint(1,20),rand.randint(1,20)) 
        elif self.advantage == 0: 
            roll = rand.randint(1,20) 
        elif self.advantage == -1: 
            roll = min(rand.randint(1,20),rand.randint(1,20)) 
        self.advantage = 0
        self.to_hit = [roll,roll+bonus]
    
    # Adds a bonus to the roll to hit 
    def bless(self, num, die): 
        for i in range(num): 
            self.to_hit[1] += rand.randint(1,die) 
        
    # Calculates the damage of an attack
    def attack(self, AC, num, dice, bonus_damage):
        temp_damage = 0 
        if self.to_hit[0] == 20: 
            self.crit = 2
            self.hit = 1
            for i in range(2*num): 
                temp_damage += rand.randint(1,dice)
            temp_damage += bonus_damage
            self.crits += 1
            self.hit_total += 1
        elif self.to_hit[1] >= AC and self.to_hit[0] != 1:  
            self.crit = 1
            self.hit = 1
            for i in range(num):
                temp_damage += rand.randint(1,dice) 
            temp_damage += bonus_damage
            self.hit_total += 1
        else: 
            self.hit = 0
        self.damage += temp_damage 
    
    # Calculates the damage of a saving throw 
    def force_save(self, DC, success_factor, num, die): 
        temp = 0 
        for i in range(num): 
            temp += rand.randint(1,die) 
        if self.to_hit[1] >= DC: 
            self.damage += int(temp*success_factor) 
        else: 
            self.damage += temp 

    # Resets some variables that need to be reset every round
    def round_reset(self): 
        self.temp_smite = self.num_smite 
        self.hit_total = 0
        self.damage = 0

    # Resets some variables that need to be reset every analysis 
    def analysis_reset(self): 
        self.crits = 0 
        self.hits = [] 

# Example characters 
Fighter = Character(0)
Rogue = Character(1) 
Barbarian = Character(0)
Cleric = Character(0)
Sorcerer = Character(1)
Cleric2 = Character(0)
Wizard = Character(0)

# Does an analysis of the average damage per round of a saving throw effect for the bonuses from -10 to +20
def save_analysis(rounds): 
    y = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    for bonus in range(-10,21): 
        Cleric2.analysis_reset() 
        Wizard.analysis_reset() 

        for l in range(rounds): 
            Cleric2.round_reset() 
            Wizard.round_reset() 

            Cleric2.roll20(bonus)
            Cleric2.force_save(13,0,1,12)
            Cleric2.hits.append(Cleric2.damage)
            Wizard.roll20(bonus)
            Wizard.force_save(15,.5,8,6)
            Wizard.hits.append(Wizard.damage)
        
        y[0].append(stat.mean(Cleric2.hits))
        y[1].append(stat.stdev(Cleric2.hits))
        y[2].append(max(Cleric2.hits))
        y[3].append(stat.mean(Wizard.hits))
        y[4].append(stat.stdev(Wizard.hits))
        y[5].append(max(Wizard.hits))

    return y

# Does an analysis of the average damage per round of a round of attacks against the ACs of 5 to 40
def attack_analysis(rounds): 
    y = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    for AC in range(5,41): 
        Fighter.analysis_reset() 
        Rogue.analysis_reset() 
        Barbarian.analysis_reset() 
        Cleric.analysis_reset()
        Sorcerer.analysis_reset()  

        for k in range(rounds): 
            Fighter.round_reset() 
            Rogue.round_reset()  
            Barbarian.round_reset() 
            Cleric.round_reset() 
            Sorcerer.round_reset()

            Fighter.roll20(5)
            Fighter.attack(AC,1,6,3)
            Fighter.roll20(5)
            Fighter.attack(AC,1,6,3)
            Fighter.hits.append(Fighter.damage)
            Rogue.roll20(6)
            Rogue.attack(AC,1,8,4) 
            Rogue.smite_dice(1,6)
            Rogue.hits.append(Rogue.damage)
            Barbarian.roll20(5)
            Barbarian.attack(AC,1,8,5)
            Barbarian.hits.append(Barbarian.damage)
            Sorcerer.roll20(6)
            Sorcerer.attack(AC,1,10,0) 
            Sorcerer.hits.append(Sorcerer.damage)
            Cleric.roll20(4)
            Cleric.attack(AC,1,6,2)
            Cleric.hits.append(Cleric.damage)
            
        y[0].append(stat.mean(Fighter.hits))
        y[1].append(stat.stdev(Fighter.hits))
        y[2].append(max(Fighter.hits))
        y[3].append(stat.mean(Rogue.hits))
        y[4].append(stat.stdev(Rogue.hits))
        y[5].append(max(Rogue.hits))
        y[6].append(stat.mean(Barbarian.hits))
        y[7].append(stat.stdev(Barbarian.hits))
        y[8].append(max(Barbarian.hits))
        y[9].append(stat.mean(Sorcerer.hits))
        y[10].append(stat.stdev(Sorcerer.hits))
        y[11].append(max(Sorcerer.hits))
        y[12].append(stat.mean(Cleric.hits))
        y[13].append(stat.stdev(Cleric.hits))
        y[14].append(max(Cleric.hits))

    return y

x_vals = [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40] 
x_vals_2 = [-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
y_vals_attack = attack_analysis(10000)
y_vals_save = save_analysis(10000) 

plt.grid(color = 'black', ls = '--', linewidth = 1)
plt.plot(x_vals,y_vals_attack[0], color = 'blue')
#plt.plot(x_vals,y_vals_attack[2], color = 'blue', ls = ':')
plt.plot(x_vals,y_vals_attack[3], color = 'green')
#plt.plot(x_vals,y_vals_attack[5], color = 'green', ls = ":")
plt.plot(x_vals,y_vals_attack[6], color = 'orange')
#plt.plot(x_vals,y_vals_attack[8], color = 'orange', ls = ':')
plt.plot(x_vals,y_vals_attack[9], color = 'brown')
#plt.plot(x_vals,y_vals_attack[11], color = 'brown', ls = ':')
plt.plot(x_vals,y_vals_attack[12], color = 'red')
#plt.plot(x_vals,y_vals_attack[14], color = 'red', ls = ':')

plt.title('Average DPR vs AC')
#plt.legend(['Fighter','Fighter Max','Rogue','Rogue Max','Barbarian','Barbarian Max','Sorcerer','Sorcerer Max','Cleric','Cleric Max'])
plt.legend(['Fighter', 'Rogue', 'Barbarian', 'Sorcerer', 'Cleric'])
plt.xlabel('AC')
plt.ylabel('Average DPR')
plt.show()

plt.grid(color = 'black', ls = '--', linewidth = 1)
plt.plot(x_vals_2,y_vals_save[0], color = 'blue')
plt.plot(x_vals_2,y_vals_save[2], color = 'blue', ls = ':')
plt.plot(x_vals_2,y_vals_save[3], color = 'green')
plt.plot(x_vals_2,y_vals_save[5], color = 'green', ls = ':')

plt.title('Average DPR vs bonus to save')
plt.legend(['Cleric2','Cleric2 Max', 'Wizard', 'Wizard Max'])
plt.xlabel('bonus to save')
plt.ylabel('Average DPR')
plt.show() 
