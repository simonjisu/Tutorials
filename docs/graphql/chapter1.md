---
title: "Chapter 1 - Welcome To GraphQL"
hide:
  - tags
tags:
  - GraphQL
---

# Welcome to GraphQL

## What is GraphQL

* 쿼리 언어, 쿼리에 대한 데이터를 받을 수 있는 런타임
* 예시: SWAPI [https://graphql.org/swapi-graphql](https://graphql.org/swapi-graphql)
* 선언형(declarative) 데이터 페칭(fetching) 언어
* 클라이언트와 서버 간의 통신 명세(스펙)
    * 명세: 한 언어의 능력과 특징이 기술되어 있음. 공통의 어휘를 제공하고, 모범 사례 설명
    * [https://graphql.org/code/](https://graphql.org/code/)
* 설계 원칙
    * **위계적**: GraphQL 쿼리는 위계성을 띈다. 필드 안에 다른 필드가 중첩 될수 있고, 쿼리와 그에 대한 반환 데이터는 형태가 서로 같음
    * **제품 중심적**: GraphQL은 클라이언트가 요구하는 데이터와 클라이언트가 지원하는 언어 및 런타임에 맞춰 동작함
    * **엄격한 타입 제한**: GraphQL 서버는 GraphQL 타입 시스템 사용. 스키마의 데이텉 포인트마다 특정 타입이 명시되며, 이를 기초로 유효성 검사를 받음
    * **클라이언트 맞춤 쿼리**: GraphQL 서버는 클라이언트 쪽에서 받아서 사용할 수 있는 데이터 제공
    * **인트로스펙티브(introspective)**: GraphQL 언어를 사용해 GraphQL 서버가 사용하는 타입 시스템에 대한 쿼리 작성 가능

## 데이터 전송의 역사

* RPC(Remote Procedure Call): 참고 [Microsoft RPC 작동 방식](https://docs.microsoft.com/ko-kr/windows/win32/rpc/how-rpc-works)
* SOAP(Simple Object Access Protocol)[^1]: XML을 사용해 메시지를 인코딩하고 HTTP를 사용해 전송함
* REST(Representional State Transfer)[^2]

## REST의 단점

* 오버페칭(Overfetching): API 호출 시 필요보다 더 많은 데이터(쓸모 없는 데이터)를 가져오는 것
* 언더페칭(Underfetching): 한 번 호출시 필요한 데이터를 가져오지 못해, 여러번 호출하는 상황
* REST 엔드포인트 관리

## 실습코드

[https://github.com/moonhighway/learning-graphql](https://github.com/moonhighway/learning-graphql)

[^1]: [Wikipedia - SOAP](https://ko.wikipedia.org/wiki/SOAP)
[^2]: [Wikipedia - REST](https://ko.wikipedia.org/wiki/REST)