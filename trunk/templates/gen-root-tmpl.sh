for i in api archive doc get mine pub ui
do
cat > root-$i.html <<EOF
{% extends "base-page" %}
{% block title %}$i root{% endblock %}
root-$i.html
{% block content %}
{% include 'developer-boilerplate' %}
{% endblock %}
EOF
done

