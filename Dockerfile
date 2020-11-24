FROM node:12 as builder
WORKDIR /usr/src/app
COPY ./front/package.json ./
RUN yarn
COPY ./front/. .
RUN yarn generate

FROM python:3.8-buster
RUN pip3 install pymongo python-dateutil
COPY --from=builder /usr/src/app/dist ./dist
COPY ./back/. .

EXPOSE 8080
CMD ["python3", "./main.py"]

