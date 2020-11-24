FROM node:12 as builder
WORKDIR /usr/src/app
COPY ./front/package.json ./
RUN yarn
COPY ./front/. .
RUN yarn generate

FROM continuumio/anaconda3:2020.07
RUN pip3 install pymongo
COPY --from=builder /usr/src/app/dist ./dist
COPY ./back/. .

EXPOSE 8080
CMD ["python3", "./main.py"]

