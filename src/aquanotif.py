a
    �~`�  �                   @   s�   d dl mZ d dlmZ d dlZd dlZe�d�Ze�d�ZeD ]RZ	e�
ee	�r@ed�e	�� eddd	�Zejjd
ed�e	�d�d� ed�  q�q@dS )�    )�listdir)�UpdaterNz\d.txtzlog/zSending {}...z.1246243249:AAEDt_r0aym991a0znWIyOIaXBGkP68HO5oT)Zuse_contextiڕ�+zlog/{}�r)ZdocumentZSuccess)�posixr   Ztelegram.extr   �re�os�compileZpolaZlistFileZfileList�search�print�formatZupdaterZbotZsend_document�open� r   r   �src/aquanotif-source.py�<module>   s   

