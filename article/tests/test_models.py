# -*- coding: utf-8 -*-
"""
This module contains base automated tests for article app models.
"""

from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from datetime import datetime

from ..models import Source, Article, Category


def create_demo_data():
    User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
    user_1 = User.objects.create_user(username='test1', password='test123321')
    user_2 = User.objects.create_user(username='test2', password='test123321')
    user_3 = User.objects.create_user(username='test3', password='test123321')

    cat1 = Category.objects.create(name='Политика')
    cat2 = Category.objects.create(name='Экономика')
    cat3 = Category.objects.create(name='Спорт')

    source_1 = Source.objects.create(
        name='Медуза',
        label='MDZ',
        url='https://meduza.ru/',
    )
    source_1.categories.add(cat1)
    source_1.categories.add(cat2)

    source_2 = Source.objects.create(
        name='Sports',
        label='SPRT',
        url='https://sports.ru/',
    )
    source_2.categories.add(cat3)

    article_1 = Article.objects.create(
        header='Статья №1',
        text='<p>Sapien, nunc quisque arcu aenean tristique pretium sociis conubia. Elit eget sit eu sociosqu auctor habitasse libero etiam conubia cubilia magnis nisl. Ac lacus libero, quam commodo fermentum magnis sapien tellus. Faucibus tellus pharetra egestas velit. Netus volutpat scelerisque elit. Pharetra sociis orci, potenti tempor cum et feugiat ultrices. Felis curae;, per aliquam penatibus tempus mollis pretium justo. Nunc sed class adipiscing non eros felis.</p><p>Semper purus id ultricies in, pharetra nisl phasellus pulvinar lacinia. Magnis quam eu facilisis semper aenean sapien duis nisi primis. Lectus natoque malesuada quis sociosqu quam sollicitudin sapien. A felis proin tristique semper justo, lobortis mattis nascetur ipsum. Nostra pulvinar volutpat phasellus, lectus odio! Ac placerat arcu leo ornare, bibendum eget. Tempor faucibus fringilla ligula massa sociis porttitor, curae; torquent non. Orci aenean rutrum lectus primis. Sit eros felis auctor. Hac etiam nibh conubia suspendisse id? Commodo viverra dictumst rhoncus et nulla ligula? Eu nunc augue augue.</p><p>Libero risus vel augue litora dapibus. Leo cursus facilisi habitant tempor. Pulvinar morbi malesuada cursus venenatis nec sit. Metus nisi netus lacinia sollicitudin. Nullam sed sem volutpat tempor habitasse! Senectus commodo gravida porta netus. Lectus nullam diam justo suspendisse fringilla consectetur class. Phasellus natoque in mauris eros felis maecenas porttitor luctus bibendum! Nunc dis mattis erat mattis pharetra magna quis parturient conubia faucibus. Condimentum scelerisque dolor a rhoncus ipsum feugiat facilisi aenean! Nam accumsan fames purus ad risus consectetur lacus vehicula fringilla eros varius purus. Nunc, magnis fringilla senectus. Nulla mauris placerat id consectetur facilisis non placerat natoque.</p><p>Cum sed rutrum mus sociis quisque tristique ullamcorper risus natoque consequat ornare. Nibh, velit metus nec ultrices mi. Purus condimentum parturient lobortis torquent diam hendrerit lobortis. Velit scelerisque massa suscipit vel. Quisque neque lacinia nostra venenatis? Suscipit litora gravida conubia suscipit fringilla quisque ad scelerisque! Iaculis leo urna a? Eu pulvinar at ad ridiculus? Fringilla eget eros placerat condimentum mollis risus. Pharetra arcu, condimentum vitae potenti montes cras euismod hendrerit mus neque montes! Felis laoreet ultricies viverra. Sagittis platea nulla himenaeos!</p><p>Bibendum metus hendrerit urna ultrices ipsum quam! Venenatis proin donec consequat? Eget suspendisse commodo suspendisse imperdiet turpis elit ridiculus ac ullamcorper class faucibus lectus? Enim mauris arcu integer turpis. Mi aptent justo commodo sollicitudin sociosqu habitant potenti augue neque habitant. Est curabitur aliquam potenti dignissim quam rhoncus ac libero purus. Sem sem euismod, sociis aliquam volutpat blandit iaculis torquent adipiscing. Suspendisse.</p>',
        url='https://site.com/article1/',
        date=datetime.fromisoformat('2020-09-28 12:17:00'),
        source=source_1
    )
    article_1.users.add(user_1)

    article_2 = Article.objects.create(
        header='Статья №2',
        text='<p>Sapien, nunc quisque arcu aenean tristique pretium sociis conubia. Elit eget sit eu sociosqu auctor habitasse libero etiam conubia cubilia magnis nisl. Ac lacus libero, quam commodo fermentum magnis sapien tellus. Faucibus tellus pharetra egestas velit. Netus volutpat scelerisque elit. Pharetra sociis orci, potenti tempor cum et feugiat ultrices. Felis curae;, per aliquam penatibus tempus mollis pretium justo. Nunc sed class adipiscing non eros felis.</p><p>Semper purus id ultricies in, pharetra nisl phasellus pulvinar lacinia. Magnis quam eu facilisis semper aenean sapien duis nisi primis. Lectus natoque malesuada quis sociosqu quam sollicitudin sapien. A felis proin tristique semper justo, lobortis mattis nascetur ipsum. Nostra pulvinar volutpat phasellus, lectus odio! Ac placerat arcu leo ornare, bibendum eget. Tempor faucibus fringilla ligula massa sociis porttitor, curae; torquent non. Orci aenean rutrum lectus primis. Sit eros felis auctor. Hac etiam nibh conubia suspendisse id? Commodo viverra dictumst rhoncus et nulla ligula? Eu nunc augue augue.</p><p>Libero risus vel augue litora dapibus. Leo cursus facilisi habitant tempor. Pulvinar morbi malesuada cursus venenatis nec sit. Metus nisi netus lacinia sollicitudin. Nullam sed sem volutpat tempor habitasse! Senectus commodo gravida porta netus. Lectus nullam diam justo suspendisse fringilla consectetur class. Phasellus natoque in mauris eros felis maecenas porttitor luctus bibendum! Nunc dis mattis erat mattis pharetra magna quis parturient conubia faucibus. Condimentum scelerisque dolor a rhoncus ipsum feugiat facilisi aenean! Nam accumsan fames purus ad risus consectetur lacus vehicula fringilla eros varius purus. Nunc, magnis fringilla senectus. Nulla mauris placerat id consectetur facilisis non placerat natoque.</p><p>Cum sed rutrum mus sociis quisque tristique ullamcorper risus natoque consequat ornare. Nibh, velit metus nec ultrices mi. Purus condimentum parturient lobortis torquent diam hendrerit lobortis. Velit scelerisque massa suscipit vel. Quisque neque lacinia nostra venenatis? Suscipit litora gravida conubia suscipit fringilla quisque ad scelerisque! Iaculis leo urna a? Eu pulvinar at ad ridiculus? Fringilla eget eros placerat condimentum mollis risus. Pharetra arcu, condimentum vitae potenti montes cras euismod hendrerit mus neque montes! Felis laoreet ultricies viverra. Sagittis platea nulla himenaeos!</p><p>Bibendum metus hendrerit urna ultrices ipsum quam! Venenatis proin donec consequat? Eget suspendisse commodo suspendisse imperdiet turpis elit ridiculus ac ullamcorper class faucibus lectus? Enim mauris arcu integer turpis. Mi aptent justo commodo sollicitudin sociosqu habitant potenti augue neque habitant. Est curabitur aliquam potenti dignissim quam rhoncus ac libero purus. Sem sem euismod, sociis aliquam volutpat blandit iaculis torquent adipiscing. Suspendisse.</p>',
        url='https://site.com/article2/',
        date=datetime.fromisoformat('2020-09-25 10:15:00'),
        source=source_2
    )
    article_2.users.add(user_2)


class SourceTest(TestCase):
    """Test class for Source model"""

    def setUp(self):
        create_demo_data()

    def test_source_creation(self):
        source_1 = Source.objects.get(url='https://meduza.ru/')
        self.assertEqual(source_1.name, 'Медуза')

    def test_unique_url_creation(self):
        with self.assertRaises(IntegrityError):
            Source.objects.create(
                name='Медуза2',
                label='MDZ2',
                url='https://meduza.ru/',
            )


class ArticleTest(TestCase):
    """Test class for Article model"""

    def setUp(self):
        create_demo_data()

    def test_article_creation(self):
        article_1 = Article.objects.get(url='https://site.com/article1/')
        self.assertEqual(article_1.header, 'Статья №1')
