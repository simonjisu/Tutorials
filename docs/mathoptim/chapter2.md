---
title: "Chapter - 2 선형 계획"
hide:
  - tags
tags:
  - 수학적 최적화
---

## 1. 선형 계획 문제

$$ \begin{aligned} \arg \min\  & c^Tx \\ \text{s.t. } & Ax^T \geq b, \\ & x \geq 0  \end{aligned}$$

where

$$\begin{aligned} \mathbf{A} &= \begin{bmatrix} a_{11} & \cdots & a_{1n} \\ \vdots & \ddots & \vdots \\ a_{m_1} & \cdots & a_{mn} \end{bmatrix} \in \Bbb{R}^{m \times n} \end{aligned}$$

$$\begin{aligned}
\mathbf{b} &= \begin{bmatrix} b_{1} \\ \vdots \\ b_m \end{bmatrix} \in \Bbb{R}^m, \mathbf{c} = \begin{bmatrix} c_{1} \\ \vdots \\ c_n \end{bmatrix} \in \Bbb{R}^n , \mathbf{x} = \begin{bmatrix} x_{1} \\ \vdots \\ x_n \end{bmatrix} \in \Bbb{R}^n
\end{aligned}$$



### 운송 계획 문제

* 제품을 m개 공장에서 n개 고객에게 납입해야 함. 각 공장의 생산량을 넘지 않는 범위에서 고객의 수요를 만족시키도록 제품을 운송하고자 함.
* 이때 운송비 함게를 최소화하기 위해서 어느 공장에서 어느 고객에거 얼마나 많은 양의 제품을 운송하는 것이 좋은가?
* 공장 $i$의 생산량 상한을 $a_i$, 고객 $j$의 수요량을 $b_j$, 공장 $i$에서 고객 $j$로의 단위량당 운송비를 $c_{ij}$, 운송량을 $x_{ij}$ 라고 하면, 다음과 같이 문제를 형식화 할 수 있다.

!!! note "운송 계획 문제"

    $$ \arg \min\ \sum_{i=1}^m \sum_{j=1}^n c_{ij}x_{ij}$$

    $$\begin{aligned}\text{s.t. } & \sum_{i=1}^n x_{ij} \leq a_i, \quad \sum_{i=1}^m x_{ij} = b_i, \quad x_{ij} \geq 0 \\ & i = 1, \dots, m, \quad j = 1, \dots, n
    \end{aligned}$$

### 일정 계획 문제

* $n$개의 작업으로 이루어지는 프로젝트가 있고, 앞에서 진행된 작업이 모두 완료되어야 다음 작업 진행 가능하다. 
* 각 작업은 기본 처리 비용이 들며, 어느 정도 비용을 추가해 어느 정도까지 날짜를 단축 할 수 있다. 
* 전체 $T$일 이내에 완료해야하는 조건으로 비용 합계를 최소화하기 위해서 각 작업의 시작일과 처리 일수를 어떻게 정해야 할까?

``` mermaid
flowchart LR;
    A[Start]:::clsA --> B1((1)):::clsB --> B2((2)):::clsB
    B2 --> B3((3)):::clsB --> B5((5)):::clsB --> B7((7)):::clsB
    B2 --> B4((4)):::clsB --> B6((6)):::clsB --> B7
    B4 --> B5
    B7 --> A2[End]:::clsA
    classDef clsA fill:#f5c414;
    classDef clsB fill:#669dfa;
```

* $i$번째 작업의 처리 일수를 $u_i$, 비용을 $c_i$, 실제 처리 일수 $p_i$라고 한다. 
* $u_i$ 대비 1일 단축할 때 발생하는 추가 비용을 $g_i$라고 하면, 작업 $i$의 비용은 $c_i + g_i(u_i - p_i)$가 된다.
* 다만, 어느 정도 단축해도 단숨에 처리가 불가능하기에 최소 처리 일수를 $l_i$라고 한다.
* 각 작업 $i$의 시작일을 $s_i$ 라고 하면, 다음과 같이 문제를 형식화 할 수 있다.

!!! note "일정 계획 문제"

    $$ \arg \min\ \sum_{i=1}^n c_i + g_i (u_i - p_i) $$

    $$\begin{aligned}\text{s.t. } & s_i + p_i \leq s_j, \quad l_i \leq p_i \leq u_i, \\
    & s_i \geq 0, \quad s_n + p_n \leq T \\
    & i = 1, \dots, n, \quad j = 1, \dots, n, \quad i \prec j
    \end{aligned}$$

### 생산 계획 문제

* 한 공장에서 $m$ 종류의 원료를 이용해 $n$ 종류의 제품을 생산함.
* 고객의 수요와 생산비가 시기에 따라 변해서, 공장 생산과 창고의 재고를 조합해 고객에게 제품을 전달하는 상황
* 생산비와 재고비의 합계를 최소화하기 위해 어느 시기에 얼마나 많은 제품을 생산해서 창고의 재고로 비축할 것인가?
* 제품 $j$를 한 단위 생산하기 위해 필요한 원료 $i$의 양을 $a_{ij}$ 라고함.
* 계획 기간을 $T$, 각 시기 $t$의 원료 $i$ 공급량을 $b_{it}$, 제품 $j$의 고객 수요량을 $d_{jt}$, 단위량당 생산비를 $c_{jt}$, 재고비를 $f_{jt}$라고 함.
* $t=0$에서 재고량을 0으로 하며, 각 기간 $t$의 제품 $j$의 생산량을 $x_{jt}$, 재고량을 $s_{jt}$라고 하면 다음과 같이 형식화 할 수 있다.

!!! note "생산 계획 문제"

    $$ \arg \min\ \sum_{j=1}^n \sum_{t=1}^T c_{jt}x_{jt} + f_{jt}s_{jt} $$

    $$\begin{aligned}\text{s.t. } 
    & \sum_{j=1}^n a_{ij}x_{jt} \leq b_{it}, \quad s_{j(t-1)} + x_{jt} - s_{jt} = d_{jt} \\
    & s_{j0} = 0, \quad x_{jt}, s_{jt} \geq 0 \\
    & i = 1, \dots, m, \quad j = 1, \dots, n, \quad t = 1, \dots, T
    \end{aligned}$$