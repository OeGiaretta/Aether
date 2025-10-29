"""
Componentes de gauges visuais para o AETHER Dashboard.

Este módulo fornece componentes visuais personalizados para exibir
dados de sensores automotivos em formato de gauges e indicadores.
"""

import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any, Optional, Tuple
import math


class AetherGauge:
    """
    Classe para criar gauges personalizados para dados automotivos.
    """
    
    @staticmethod
    def create_rpm_gauge(value: float, 
                        min_val: float = 0, 
                        max_val: float = 8000,
                        title: str = "RPM") -> go.Figure:
        """
        Cria um gauge para RPM do motor.
        
        Args:
            value: Valor atual do RPM
            min_val: Valor mínimo
            max_val: Valor máximo
            title: Título do gauge
            
        Returns:
            Figura do Plotly
        """
        # Definir cores baseadas no valor
        if value < max_val * 0.5:
            color = "green"
        elif value < max_val * 0.75:
            color = "orange"
        else:
            color = "red"
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': title},
            delta = {'reference': max_val * 0.6},
            gauge = {
                'axis': {'range': [min_val, max_val]},
                'bar': {'color': color},
                'steps': [
                    {'range': [min_val, max_val * 0.5], 'color': "lightgray"},
                    {'range': [max_val * 0.5, max_val * 0.75], 'color': "yellow"},
                    {'range': [max_val * 0.75, max_val], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': max_val * 0.9
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            font={'color': "darkblue", 'family': "Arial Black"}
        )
        
        return fig
    
    @staticmethod
    def create_speed_gauge(value: float,
                          min_val: float = 0,
                          max_val: float = 240,
                          title: str = "Velocidade") -> go.Figure:
        """
        Cria um gauge para velocidade.
        
        Args:
            value: Valor atual da velocidade
            min_val: Valor mínimo
            max_val: Valor máximo
            title: Título do gauge
            
        Returns:
            Figura do Plotly
        """
        # Definir cores baseadas no valor
        if value < 60:
            color = "green"
        elif value < 120:
            color = "yellow"
        else:
            color = "red"
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': f"{title} (km/h)"},
            gauge = {
                'axis': {'range': [min_val, max_val]},
                'bar': {'color': color},
                'steps': [
                    {'range': [min_val, 60], 'color': "lightgreen"},
                    {'range': [60, 120], 'color': "yellow"},
                    {'range': [120, max_val], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 140
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            font={'color': "darkblue", 'family': "Arial Black"}
        )
        
        return fig
    
    @staticmethod
    def create_temperature_gauge(value: float,
                                min_val: float = -40,
                                max_val: float = 130,
                                title: str = "Temperatura") -> go.Figure:
        """
        Cria um gauge para temperatura.
        
        Args:
            value: Valor atual da temperatura
            min_val: Valor mínimo
            max_val: Valor máximo
            title: Título do gauge
            
        Returns:
            Figura do Plotly
        """
        # Definir cores baseadas no valor
        if value < 80:
            color = "blue"
        elif value < 100:
            color = "green"
        elif value < 110:
            color = "yellow"
        else:
            color = "red"
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': f"{title} (°C)"},
            gauge = {
                'axis': {'range': [min_val, max_val]},
                'bar': {'color': color},
                'steps': [
                    {'range': [min_val, 80], 'color': "lightblue"},
                    {'range': [80, 100], 'color': "lightgreen"},
                    {'range': [100, 110], 'color': "yellow"},
                    {'range': [110, max_val], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 105
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            font={'color': "darkblue", 'family': "Arial Black"}
        )
        
        return fig
    
    @staticmethod
    def create_percentage_gauge(value: float,
                               title: str = "Percentual",
                               unit: str = "%") -> go.Figure:
        """
        Cria um gauge para valores percentuais.
        
        Args:
            value: Valor atual (0-100)
            title: Título do gauge
            unit: Unidade do valor
            
        Returns:
            Figura do Plotly
        """
        # Definir cores baseadas no valor
        if value < 30:
            color = "green"
        elif value < 70:
            color = "yellow"
        else:
            color = "red"
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': f"{title} ({unit})"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 30], 'color': "lightgreen"},
                    {'range': [30, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            font={'color': "darkblue", 'family': "Arial Black"}
        )
        
        return fig


class AetherIndicator:
    """
    Classe para criar indicadores visuais simples.
    """
    
    @staticmethod
    def create_status_card(title: str, 
                          value: Any, 
                          unit: str = "",
                          status: str = "normal",
                          delta: Optional[float] = None) -> None:
        """
        Cria um card de status visual.
        
        Args:
            title: Título do card
            value: Valor a ser exibido
            unit: Unidade do valor
            status: Status (normal, warning, error)
            delta: Variação do valor (opcional)
        """
        # Definir cores baseadas no status
        if status == "error":
            color = "red"
            icon = "🔴"
        elif status == "warning":
            color = "orange"
            icon = "🟡"
        else:
            color = "green"
            icon = "🟢"
        
        # Criar container com estilo
        with st.container():
            st.markdown(f"""
            <div style="
                border: 2px solid {color};
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                background-color: rgba(255, 255, 255, 0.1);
            ">
                <h4 style="color: {color}; margin: 0;">{icon} {title}</h4>
                <h2 style="color: {color}; margin: 10px 0;">{value:.1f} {unit}</h2>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def create_progress_bar(value: float,
                           max_value: float,
                           title: str,
                           color: str = "blue") -> None:
        """
        Cria uma barra de progresso visual.
        
        Args:
            value: Valor atual
            max_value: Valor máximo
            title: Título da barra
            color: Cor da barra
        """
        percentage = (value / max_value) * 100
        
        st.markdown(f"""
        <div style="margin: 10px 0;">
            <p style="margin: 0; font-weight: bold;">{title}</p>
            <div style="
                background-color: #f0f0f0;
                border-radius: 10px;
                height: 20px;
                margin: 5px 0;
            ">
                <div style="
                    background-color: {color};
                    height: 100%;
                    width: {min(percentage, 100)}%;
                    border-radius: 10px;
                    transition: width 0.3s ease;
                "></div>
            </div>
            <p style="margin: 0; font-size: 12px; color: #666;">
                {value:.1f} / {max_value:.1f} ({percentage:.1f}%)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_alert_box(message: str, alert_type: str = "info") -> None:
        """
        Cria uma caixa de alerta.
        
        Args:
            message: Mensagem do alerta
            alert_type: Tipo do alerta (info, warning, error, success)
        """
        # Definir ícones e cores
        icons = {
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "❌",
            "success": "✅"
        }
        
        colors = {
            "info": "#3498db",
            "warning": "#f39c12",
            "error": "#e74c3c",
            "success": "#27ae60"
        }
        
        icon = icons.get(alert_type, "ℹ️")
        color = colors.get(alert_type, "#3498db")
        
        st.markdown(f"""
        <div style="
            background-color: {color}20;
            border-left: 4px solid {color};
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        ">
            <p style="margin: 0; color: {color}; font-weight: bold;">
                {icon} {message}
            </p>
        </div>
        """, unsafe_allow_html=True)
