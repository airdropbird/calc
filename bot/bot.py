import asyncio
import discord
import os
from discord.ext import commands
from discord_components import *
from dotenv import load_dotenv

class CalcBot:
    def __init__(self):
        pass
        
    def run():
        client = commands.Bot(command_prefix='.', intents=discord.Intents.all())
        load_dotenv()

        @client.event
        async def on_ready():
            DiscordComponents(client)
            print(f"{client.user} is Ready")

        @client.command()
        async def calc(ctx):
            keys = [
                [Button(style=ButtonStyle.blue, label='('),
                 Button(style=ButtonStyle.blue, label=')'),
                 Button(style=ButtonStyle.blue, label='⌫'),
                 Button(style=ButtonStyle.red, label='AC')],
                [Button(style=ButtonStyle.grey, label='7'),
                 Button(style=ButtonStyle.grey, label='8'),
                 Button(style=ButtonStyle.grey, label='9'),
                 Button(style=ButtonStyle.blue, label='÷')],
                [Button(style=ButtonStyle.grey, label='4'),
                 Button(style=ButtonStyle.grey, label='5'),
                 Button(style=ButtonStyle.grey, label='6'),
                 Button(style=ButtonStyle.blue, label='×')],
                [Button(style=ButtonStyle.grey, label='1'),
                 Button(style=ButtonStyle.grey, label='2'),
                 Button(style=ButtonStyle.grey, label='3'),
                 Button(style=ButtonStyle.blue, label='-')],
                [Button(style=ButtonStyle.grey, label='0'),
                 Button(style=ButtonStyle.grey, label='.'),
                 Button(style=ButtonStyle.green, label='='),
                 Button(style=ButtonStyle.blue, label='+')],
            ]
            keys_disabled = [
                [Button(style=ButtonStyle.blue, label='(', disabled=True),
                 Button(style=ButtonStyle.blue, label=')', disabled=True),
                 Button(style=ButtonStyle.blue, label='⌫', disabled=True),
                 Button(style=ButtonStyle.red, label='AC', disabled=True)],
                [Button(style=ButtonStyle.grey, label='7', disabled=True),
                 Button(style=ButtonStyle.grey, label='8', disabled=True),
                 Button(style=ButtonStyle.grey, label='9', disabled=True),
                 Button(style=ButtonStyle.blue, label='÷', disabled=True)],
                [Button(style=ButtonStyle.grey, label='4', disabled=True),
                 Button(style=ButtonStyle.grey, label='5', disabled=True),
                 Button(style=ButtonStyle.grey, label='6', disabled=True),
                 Button(style=ButtonStyle.blue, label='×', disabled=True)],
                [Button(style=ButtonStyle.grey, label='1', disabled=True),
                 Button(style=ButtonStyle.grey, label='2', disabled=True),
                 Button(style=ButtonStyle.grey, label='3', disabled=True),
                 Button(style=ButtonStyle.blue, label='-', disabled=True)],
                [Button(style=ButtonStyle.grey, label='0', disabled=True),
                 Button(style=ButtonStyle.grey, label='.', disabled=True),
                 Button(style=ButtonStyle.green, label='=', disabled=True),
                 Button(style=ButtonStyle.blue, label='+', disabled=True)],
            ]
            calc_msg = await ctx.send(embed=discord.Embed(description='```                              0```',
                                                          colour=discord.Colour.from_rgb(255, 215, 0)), components=keys)

            def check(m):
                return m.channel == ctx.channel and m.author == ctx.author

            final_equation = ""
            previous_input = ""
            equation_valid = True
            format_error = False
            while True:
                try:
                    res = await client.wait_for("button_click", check=check, timeout=60)
                except asyncio.TimeoutError:
                    await calc_msg.edit(components=keys_disabled)
                    return
                await res.respond(type=6)

                current_input = res.component.label
                if current_input == "=":
                    if not equation_valid:
                        continue
                    if final_equation == "":
                        final_equation = "0"

                    def is_number(item):
                        try:
                            float(item)
                            return True
                        except ValueError:
                            return False

                    def set_up_list():
                        a_list = []
                        for item in final_equation:
                            a_list.append(item)
                        count = 0
                        while count < len(a_list) - 1:
                            if is_number(a_list[count]) and is_number(a_list[count + 1]):
                                a_list[count] += a_list[count + 1]
                                del a_list[count + 1]
                            elif is_number(a_list[count]) and a_list[count + 1] == ".":
                                try:
                                    x = a_list[count + 2]
                                except IndexError:
                                    format_error = True
                                if is_number(a_list[count + 2]):
                                    a_list[count] += a_list[count + 1] + a_list[count + 2]
                                    del a_list[count + 2]
                                    del a_list[count + 1]
                            else:
                                count += 1
                        return a_list

                    def perform_operation(n1, operand, n2):
                        if operand == "+":
                            return str(float(n1) + float(n2))
                        elif operand == "-":
                            return str(float(n1) - float(n2))
                        elif operand == "×":
                            return str(float(n1) * float(n2))
                        elif operand == "÷":
                            try:
                                n = str(float(n1) / float(n2))
                                return n
                            except ZeroDivisionError:
                                print(f"Zero Division Error!")

                    expression = set_up_list()
                    emergency_count = 0
                    P = ["(", ")"]
                    while len(expression) != 1:
                        count = 0
                        while count < len(expression) - 1:
                            if expression[count] == "(":
                                if expression[count + 2] == ")":
                                    del expression[count + 2]
                                    del expression[count]
                            count += 1
                        count = 0
                        while count < len(expression) - 1:
                            if expression[count] in ["×", "÷"] and not (
                                    expression[count + 1] in P or expression[count - 1] in P):
                                expression[count - 1] = perform_operation(expression[count - 1], expression[count],
                                                                          expression[count + 1])
                                del expression[count + 1]
                                del expression[count]
                            count += 1
                        count = 0
                        while count < len(expression) - 1:
                            if expression[count] in ["+", "-"] and not (
                                    expression[count + 1] in P or expression[count - 1] in P):
                                expression[count - 1] = perform_operation(expression[count - 1], expression[count],
                                                                          expression[count + 1])
                                del expression[count + 1]
                                del expression[count]
                            count += 1
                        emergency_count += 1
                        if emergency_count >= 1000:
                            await calc_msg.edit(embed=discord.Embed(description="```         Operation was bugged!!```",
                                                                    colour=discord.Colour.from_rgb(255, 215, 0)),
                                                components=keys_disabled)
                            return
                    if expression[0] is None:
                        await calc_msg.edit(embed=discord.Embed(description="```   You tried to divide by zero!!```",
                                                                colour=discord.Colour.from_rgb(255, 215, 0)),
                                            components=keys_disabled)
                        return
                    elif format_error:
                        await calc_msg.edit(embed=discord.Embed(description="```      Error in your formatting!!```",
                                                                colour=discord.Colour.from_rgb(255, 215, 0)),
                                            components=keys_disabled)
                        return
                    if float(expression[0]).is_integer():
                        final_equation = str(round(float(expression[0])))
                    else:
                        final_equation = str(float(expression[0]))
                elif current_input == "AC":
                    final_equation = ""
                    await calc_msg.edit(embed=discord.Embed(description='```                              0```',
                                                            colour=discord.Colour.from_rgb(255, 215, 0)),
                                        components=keys)
                    continue
                elif current_input == "⌫":
                    if final_equation == "":
                        continue
                    final_equation = final_equation[0:len(final_equation) - 1]
                elif (previous_input in ["×", "÷", "+", "-", ""] and current_input == ".") or (
                        previous_input == "." and current_input in ["×", "÷", "+", "-"]) or (
                        previous_input == "" and current_input in ["×", "÷", "+", "-"]) or (
                        previous_input in ["×", "÷", "+", "-"] and current_input == "."):
                    final_equation = final_equation + "0" + current_input
                elif previous_input == ")" and current_input == ".":
                    final_equation = final_equation + "×0" + current_input
                elif (previous_input in ["1", "2", "3", "4", "5", "6", "7", "8", "9",
                                         "0"] and current_input == "(") or (
                        previous_input == ")" and current_input in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]):
                    final_equation = final_equation + "×" + current_input
                elif (previous_input in ["×", "÷", "+", "-"] and current_input == ")") or (
                        previous_input == "(" and current_input in [")", "×", "÷", "+", "-", "%"]):
                    continue
                elif previous_input in ["×", "÷", "+", "-"] and current_input in ["×", "÷", "+", "-"]:
                    final_equation = final_equation[0:len(final_equation) - 1]
                    final_equation = final_equation + current_input
                else:
                    final_equation = final_equation + current_input

                if len(final_equation) > 31:
                    await calc_msg.edit(embed=discord.Embed(description="```       Operation was too long!!```",
                                                            colour=discord.Colour.from_rgb(255, 215, 0)),
                                        components=keys_disabled)
                    return
                len_whitespace = 31 - len(final_equation)
                whitespace = ""
                while len_whitespace != 0:
                    whitespace = " " + whitespace
                    len_whitespace = len_whitespace - 1
                await calc_msg.edit(embed=discord.Embed(description=f'```{whitespace}{final_equation}```',
                                                        colour=discord.Colour.from_rgb(255, 215, 0)), components=keys)
                if current_input in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "×", "÷", "+", "-"]:
                    previous_input = current_input

        client.run(os.getenv("TOKEN"), reconnect=True)


