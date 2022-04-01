# Generated by Django 4.0.3 on 2022-03-31 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quests', '0003_rename_nota_tentativa_pontos_alternativa_certa'),
    ]

    operations = [
        migrations.AddField(
            model_name='tentativa',
            name='respostas',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='quests.alternativa'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Resposta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alternativa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quests.alternativa')),
                ('pergunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quests.pergunta')),
            ],
        ),
    ]
